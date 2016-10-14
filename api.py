# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


# TODO
# case where you already played a correct letter

import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import User, Game
from models import StringMessage, NewGameForm, GameForm, PlayTurnForm
from utils import get_by_urlsafe, validate_input


USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
PLAY_TURN_REQUEST = endpoints.ResourceContainer(PlayTurnForm, 
                                                urlsafe_game_key=messages.StringField(1))




@endpoints.api(name='hangman', version='v1')
class HangmanApi(remote.Service):
    """Game API"""


    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))


    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='create_new_game_api_name',
                      http_method='POST')
    def create_new_game_api(self, request):
        """ Create a new game. Requires an exiting user"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException('There is no user with that name!')
        try:
            game = Game.create_new_game_models(user.key, request.answer, request.strikes)
        except ValueError:
            raise endpoints.BadRequestException('You really need a positive number of strikes')
        input_validation = validate_input(game.answer)
        if input_validation[0] == True:
            return game.to_form('Have fun playing Hangman!')
        else:
            raise endpoints.BadRequestException(input_validation[1])
        # The taskqueue job will go here


    @endpoints.method(request_message=PLAY_TURN_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='play_turn_api_name',
                      http_method='PUT')
    def play_turn_api(self, request):
        

        """ Process user input"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        msg = ""

        """ Validate game status"""
        if game.game_over == True:
            msg = "This game is already over!"
            raise endpoints.BadRequestException(msg)

        # Validate user input
        input_validation = validate_input(request.guess, 1)
        if input_validation[0] == False:
            raise endpoints.BadRequestException(input_validation[1])
        else:
        # Test user input against answer
            request.guess = request.guess.upper()
            answer_list = list(game.answer)
            current_game_list = list(game.current_game.replace(" ",""))
            if request.guess in answer_list:
                for i in answer_list:
                    if request.guess== i:
                        for j in range(0,len(current_game_list)):
                            if answer_list[j] == i:
                                current_game_list[j]= request.guess
                msg += "Good guess! | "
                # print "current_game_list: " + str(current_game_list)
                game.current_game = ""
                for k in range(0,len(current_game_list)):
                    game.current_game += str(current_game_list[k]) + " "

                # print "current_game_list: " + str(current_game_list)
                if current_game_list == answer_list:
                    game.game_won = True
                    game.game_over = True
            else:
                game.strikes_left -= 1
                msg += "Wrong guess... | "
                if game.strikes_left == 0:
                    game.game_over = True
                    game.game_won = False

            game.put()

            msg += game.current_game + " | " 
            msg += "Strike(s) left: " + str(game.strikes_left) + " | "

            if game.game_over == 1:
                if game.game_won == 1:
                    msg += "YOU WON!"
                if game.game_won == 0:
                    msg += "YOU LOST!"
            else:
                msg += "Carry on!"
        return game.to_form(msg)






api = endpoints.api_server([HangmanApi])
