
import endpoints
import math

from models import HistoryRecord


def rate_game(score):
    """This function rates the game after a win"""
    final_score = int((math.pow(score.unique_letters, score.unique_letters) *
                      (1 - (score.mistakes_made / score.unique_letters))))
    return final_score


def validate_guess(game, user_guess):
    """ Returns a boolean value as to whether the user guess is correct
    or not or throws an exception if the letter has already been played"""
    answer_list = list(game.answer)
    current_game_list = list(game.current_game.replace(" ", ""))

    if user_guess in current_game_list:
        msg = "You already played that letter"
        raise endpoints.BadRequestException(msg)

    if user_guess in answer_list:
        return True
    else:
        return False


def handle_right_answer(user, game, score, user_guess):
    """ Handles a correct user entry and returns a dictionary containing the
    game in its current state as well as the endpoint message"""
    current_game_list = list(game.current_game.replace(" ", ""))
    answer_list = list(game.answer)

    for i in answer_list:
        if user_guess == i:
            for j in range(0, len(current_game_list)):
                if answer_list[j] == i:
                    current_game_list[j] = user_guess
    result = "Good guess"  # will be passed into the history record
    game.current_game = ""
    for k in range(0, len(current_game_list)):
        game.current_game += str(current_game_list[k]) + " "

    if current_game_list == answer_list:
        game_state = end_game(user, game, score, True)
        user = game_state.get('user')
        game = game_state.get('game')
        score = game_state.get('score')
    game_state = update_values(user, game, score, result, user_guess)

    return game_state


def handle_wrong_answer(user, game, score, user_guess):
    """ Handles an incorrect user entry and returns a dictionary containing the
    game in its current state as well as the endpoint message"""
    game.strikes_left -= 1
    game.mistakes_made += 1
    score.mistakes_made += 1
    user_guess = user_guess
    result = "Wrong guess"  # will be passed into the history record
    if game.strikes_left == 0:
        game_state = end_game(user, game, score, False)
        user = game_state.get('user')
        game = game_state.get('game')
        score = game_state.get('score')

    game_state = update_values(user, game, score, result, user_guess)

    return game_state


# def end_game(user, game, score, game_won, user_guess):
def end_game(user, game, score, game_won):
    """ Method finalises the game and updates the various entities"""
    if game_won is True:
        game.game_won = True
        game.game_over = True
        score.game_status = "Won"
        score.final_score = rate_game(score)
        user.total_score += score.final_score
    else:
        game.game_over = True
        game.game_won = False

    game_state = {'user': user, 'game': game, 'score': score}
    return game_state


def build_message(history_record, game):
    """Builds the endpoint message from the game and current history record"""
    msg = ""
    if history_record[0].result == 'Good guess':
        msg += "Good guess! | "
    else:
        msg += "Wrong guess... | "

    msg += game.current_game + " | "
    msg += "Strike(s) left: " + str(game.strikes_left) + " | "

    if game.game_over is False:
        msg += "Carry on!"
    if game.game_over is True:
        if game.game_won is True:
            msg += "YOU WON!"
        else:
            msg += "YOU LOST!"

    return msg


def update_values(user, game, score, result, user_guess):
    """ Saves all entities to the datastore at the end of a turn and
    returns a dictionary containinig the game in its current state as well
    as the endpoint message"""
    # msg = message
    game.game_sequence += 1

    history_record = [HistoryRecord(play_sequence=game.game_sequence,
                                    action="Player played",
                                    user_entry=user_guess,
                                    result=result,
                                    current_game=game.current_game,
                                    game_over=game.game_over,
                                    game_won=game.game_won,
                                    game_cancelled=game.game_cancelled)]

    game.game_history += history_record
    game.put()
    if score:
        score.put()
    user.put()

    msg = build_message(history_record, game)

    game_state = {'game': game, 'msg': msg}

    return game_state
