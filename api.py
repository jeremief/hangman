# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


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

        # Validate user input
        input_validation = validate_input(request.guess, 1)
        if input_validation[0] == False:
            raise endpoints.BadRequestException(input_validation[1])
        else:
        # Test user input against answer
            if user_input_valid == 1:
                if game.guess in answer:
                    for i in answer:
                        if game.guess== i:
                            for j in range(0,len(current_game)):
                                if answer[j] == i:
                                    current_game[j]= user_input
                    print "CORRECT"
                    if current_game == answer:
                        won = 1
                        game_over = 1
                        display_current_game(current_game)
                else:
                    print "WRONG"
                    strikes_left -= 1
                    print " "
                    if strikes_left == 0 :
                        game_over = 1
                        won = 0
                game_over = 1


            if won == 1:
                print "YOU WON"       
            if won == 0 and game_cancelled == 0:
                print "YOU LOST"





api = endpoints.api_server([HangmanApi])
