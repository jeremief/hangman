import math

from models import User, HistoryRecord, Game, Score


def rate_game(score):
    """This function rates the game after a win"""
    final_score = int((math.pow(score.unique_letters, score.unique_letters) * 
                  (1-(score.mistakes_made / score.unique_letters))))
    return final_score
