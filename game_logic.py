
import endpoints
import math

from models import User, HistoryRecord, Game, Score


def rate_game(score):
    """This function rates the game after a win"""
    final_score = int((math.pow(score.unique_letters, score.unique_letters) * 
                  (1-(score.mistakes_made / score.unique_letters))))
    return final_score


def validate_guess(game, user_guess):
    """ Returns a boolean value as to whether the user guess is correct 
    or not or throws an exception if the letter has already been played"""
    answer_list = list(game.answer)
    current_game_list = list(game.current_game.replace(" ",""))

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
    current_game_list = list(game.current_game.replace(" ",""))
    answer_list = list(game.answer)

    for i in answer_list:
        if user_guess == i:
            for j in range(0,len(current_game_list)):
                if answer_list[j] == i:
                    current_game_list[j]= user_guess
    # msg = "Good guess! | "
    result = "Good guess" # will be passed into the history record
    game.current_game = ""
    for k in range(0,len(current_game_list)):
        game.current_game += str(current_game_list[k]) + " "

    if current_game_list == answer_list:
        # game_state = end_game(user, game, score, True, msg, user_guess)
        game_state = end_game(user, game, score, True, user_guess)
        user = game_state.get('user')
        game = game_state.get('game')
        score = game_state.get('score')
        msg = game_state.get('msg')
    # game_state = update_values(user, game, score, result, msg, user_guess)
    game_state = update_values(user, game, score, result, user_guess)

    return game_state


def handle_wrong_answer(user, game, score, user_guess):
    """ Handles an incorrect user entry and returns a dictionary containing the 
    game in its current state as well as the endpoint message"""
    game.strikes_left -= 1
    game.mistakes_made += 1
    score.mistakes_made += 1
    user_guess = user_guess
    # msg = "Wrong guess... | "
    result = "Wrong guess" # will be passed into the history record
    if game.strikes_left == 0:
        # game_state = end_game(user, game, score, False, msg, user_guess)
        game_state = end_game(user, game, score, False, user_guess)
        user = game_state.get('user')
        game = game_state.get('game')
        score = game_state.get('score')
        msg = game_state.get('msg')

    # game_state = update_values(user, game, score, result, msg, user_guess)
    game_state = update_values(user, game, score, result, user_guess)

    return game_state


# def end_game(user, game, score, game_won, message, user_guess):
def end_game(user, game, score, game_won, user_guess):
    """ Method finalises the game and updates the various entities"""
    # msg = message
    if game_won == True:
        game.game_won = True
        game.game_over = True
        score.game_over = True
        score.game_status = "Won"
        score.final_score = rate_game(score)
        user.total_score += score.final_score
    else:
        game.game_over = True
        game.game_won = False
        score.game_over = True

    # game_state = {'user':user, 'game':game, 'score':score, 'msg':msg}
    game_state = {'user':user, 'game':game, 'score':score}
    return game_state


def build_message(history_record, game):
    """Builds the endpoint message from the history record"""
    msg = ""
    if history_record[0].result == 'Good guess':
        msg += "Good guess! | "
    else:
        msg += "Wrong guess... | "

    msg += game.current_game + " | " 
    msg += "Strike(s) left: " + str(game.strikes_left) + " | "

    if game.game_over == False:
        msg += "Carry on!"
    if game.game_over == True:
        if game.game_won == True:
            msg += "YOU WON!"
        else:
            msg += "YOU LOST!"

    return msg


# def update_values(user, game, score, result, message, user_guess):
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
    score.put()
    user.put()

    msg = build_message(history_record, game)

    # msg += game.current_game + " | " 
    # msg += "Strike(s) left: " + str(game.strikes_left) + " | "

    # if game.game_over == False:
    #     msg += "Carry on!"
    # if game.game_over == True:
    #     if game.game_won == True:
    #         msg += "YOU WON!"
    #     else:
    #         msg += "YOU LOST!"

    game_state = {'game': game, 'msg': msg}

    return game_state
    
