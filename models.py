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
    email = ndb.StringProperty(required=True)
    total_score = ndb.IntegerProperty(default=0)

    def to_form(self):
        """Returns a UserForm representation of a user"""
        form = UserForm()
        form.user_name = self.name
        form.total_score = self.total_score
        return form


class HistoryRecord(ndb.Model):
    """docstring for HistoryRecord"""
    play_sequence = ndb.IntegerProperty(required=True)
    action = ndb.StringProperty(required=True)
    user_entry = ndb.StringProperty(required=True)
    result = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    current_game = ndb.StringProperty(required=True)
    game_over = ndb.BooleanProperty(required=True)
    game_won = ndb.BooleanProperty(required=True)
    game_cancelled = ndb.BooleanProperty(required=True)  


class Game(ndb.Model):
    """Game structure"""
    user = ndb.KeyProperty(required=True, kind='User')
    answer = ndb.StringProperty(required=True)
    strikes_left = ndb.IntegerProperty (required=True)
    mistakes_made = ndb.IntegerProperty(required=True)
    game_over = ndb.BooleanProperty(required=True)
    game_won = ndb.BooleanProperty(required=True)
    game_cancelled = ndb.BooleanProperty(required=True)
    current_game = ndb.StringProperty(required=True)
    game_sequence = ndb.IntegerProperty(required=True, default=1)
    game_history = ndb.StructuredProperty(HistoryRecord, repeated=True)

    @classmethod
    def create_new_game_models(cls, user, answer, strikes, history_record):
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
                    mistakes_made=0,
                    game_over=False,
                    game_won=False,
                    game_cancelled=False,
                    current_game=current_game,
                    game_history=history_record)
        game.game_history[0].current_game = game.current_game
        game.put()
        return game

    def to_form(self, message=""):
        """ Returns a GameForm representation of the game """
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.strikes = self.strikes_left
        form.mistakes = self.mistakes_made
        form.game_over = self.game_over
        form.game_won = self.game_won
        form.game_cancelled = self.game_cancelled
        form.message = message
        return form

    def to_history_form(self, i):
        """ Returns a history form"""
        form = HistoryForm()
        form.sequence = self.game_history[i].play_sequence
        form.action = self.game_history[i].action
        form.result = self.game_history[i].result
        form.user_entry = self.game_history[i].user_entry
        form.current_game = self.game_history[i].current_game
        form.game_over = self.game_history[i].game_over
        form.game_won = self.game_history[i].game_won
        form.game_cancelled = self.game_history[i].game_cancelled
        return form



class Score (ndb.Model):
    """Score keeping structure"""
    user = ndb.KeyProperty(required=True, kind='User')
    game = ndb.KeyProperty(required=True, kind='Game')
    unique_letters = ndb.IntegerProperty(required=True)
    mistakes_made = ndb.IntegerProperty(required=True, default=0)
    game_over = ndb.BooleanProperty(required=True, default=False)
    game_status = ndb.StringProperty(required=True, default='In progress')
    final_score = ndb.IntegerProperty(required=True, default=0)

    @classmethod
    def create_new_score_models(cls, user, game):
        
        count_unique_letters = 0
        unique_letters = ""
        game_letters = list(game.answer)

        for i in range(0, len(game_letters)):
            if game_letters[i] not in unique_letters:
                unique_letters += game_letters[i]
        count_unique_letters = len(unique_letters)

        score = Score(user=user.key,
                      game=game.key,
                      unique_letters=count_unique_letters,
                      mistakes_made=0,
                      game_over=False,
                      game_status='In  progress',
                      final_score=0)
        score.put()

    def to_form(self):
        form = ScoreForm()
        form.user_name = self.user.get().name
        form.urlsafe_key = self.key.urlsafe()
        form.unique_letters = self.unique_letters
        form.mistakes_made = self.mistakes_made
        form.game_over = self.game_over
        form.game_status = self.game_status
        form.final_score = self.final_score
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
    mistakes = messages.IntegerField(3, required=True)
    game_over = messages.BooleanField(4, required=True)
    game_won = messages.BooleanField(5, required=True)
    game_cancelled = messages.BooleanField(6, required=True)
    message = messages.StringField(7, required=True)
    user_name = messages.StringField(8, required=True)


class PlayTurnForm(messages.Message):
    """docstring for PlayTurnForm"""
    guess = messages.StringField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm: used to return a response containing a game's score"""
    user_name = messages.StringField(1, required=True) 
    urlsafe_key = messages.StringField(2, required=True)
    unique_letters = messages.IntegerField(3, required=True)
    mistakes_made = messages.IntegerField(4, required=True)
    game_over = messages.BooleanField(5, required=True)
    game_status = messages.StringField(6, required=True)
    final_score = messages.IntegerField(7, required=True)


class ScoreForms(messages.Message):
    """Returns multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class GameForms(messages.Message):
    """Returns multiple GameForms"""
    items = messages.MessageField(GameForm, 1, repeated=True)
        

class UserForm(messages.Message):
    """docstring for UserForm"""
    user_name = messages.StringField(1, required=True)
    total_score = messages.IntegerField(2, required=True)


class UserForms(messages.Message):
    """Returns multiple UserForms"""
    items = messages.MessageField(UserForm, 1, repeated=True)
        

class HistoryForm(messages.Message):
    """HistoryForm"""
    sequence = messages.IntegerField(1, required=True)
    action = messages.StringField(2, required=True)
    user_entry = messages.StringField(3, required=True)
    result = messages.StringField(4, required=True)
    current_game = messages.StringField(5, required=True)
    game_over = messages.BooleanField(6, required=True)
    game_won = messages.BooleanField(7, required=True)
    game_cancelled = messages.BooleanField(8, required=True)


class HistoryForms(messages.Message):
    """Returns multiple HistoryForms"""
    items = messages.MessageField(HistoryForm, 1, repeated=True)
        
                                  
        
        


        
        
        
