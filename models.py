"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email =ndb.StringProperty()


class Game(ndb.Model):
    """Game structure"""
    user = ndb.KeyProperty(required=True, kind='User')
    answer = ndb.StringProperty(required=True)
    strikes_left = ndb.IntegerProperty (required=True)
    game_over = ndb.BooleanProperty(required=True)
    game_won = ndb.BooleanProperty(required=True)
    game_cancelled = ndb.BooleanProperty(required=True)
    current_game = ndb.StringProperty(required=True)

    @classmethod
    def create_new_game_models(cls, user, answer, strikes):
        """ This method creates a new game"""
        if strikes <= 0:
            raise ValueError("You need a positive number of strikes")

        i = 0
        current_game = ""
        while i < len(answer):
            current_game += "_ "
            i += 1 

        game = Game(user=user,
                    answer=answer.upper(),
                    strikes_left=int(strikes),
                    game_over=False,
                    game_won=False,
                    game_cancelled=False,
                    current_game=current_game)
        game.put()
        return game

    def to_form(self, message):
        """ Returns a GameForm representation of the game """
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.strikes = self.strikes_left
        form.game_over = self.game_over
        form.game_won = self.game_won
        form.game_cancelled = self.game_cancelled
        form.message = message
        return form


class StringMessage(messages.Message):
    """StringMessage-- used to return a single string message"""
    message = messages.StringField(1, required=True)


class NewGameForm(messages.Message):
    """ NewGameForm: used to capture the new game request. It will then be used 
    to post in """
    user_name = messages.StringField(1, required=True)
    answer = messages.StringField(2, required=True)
    strikes = messages.IntegerField(3, default=5)


class GameForm(messages.Message):
    """GameForm: used to return a response containing the game current state"""
    urlsafe_key = messages.StringField(1, required=True)
    strikes = messages.IntegerField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    game_won = messages.BooleanField(4, required=True)
    game_cancelled = messages.BooleanField(5, required=True)
    message = messages.StringField(6, required=True)
    user_name = messages.StringField(7, required=True)


class PlayTurnForm(messages.Message):
    """docstring for PlayTurnForm"""
    guess = messages.StringField(1, required=True)
        
        
        
