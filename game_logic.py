# import logging
import endpoints
import math
# from google.appengine.ext import ndb

from models import User, HistoryRecord, Game, Score


def rate_game(score):
    """This function rates the game after a win"""
    final_score = int((math.pow(score.unique_letters, score.unique_letters) * 
                  (1-(score.mistakes_made / score.unique_letters))))
    return final_score


def validate_guess(game, user_guess):
    """ Returns a boolean value as to whether the user guess is correct 
    or not"""
    answer_list = list(game.answer)
    current_game_list = list(game.current_game.replace(" ",""))

    if user_guess in current_game_list:
        msg = "You already played that letter"
        raise endpoints.BadRequestException(msg)
    
    if user_guess in answer_list:
        return True
    else:
        return False