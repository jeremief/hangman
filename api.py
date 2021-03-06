# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


import endpoints

from protorpc import remote, messages

from models import User, HistoryRecord, Game, Score
from models import (StringMessage,
                    NewGameForm,
                    GameForm,
                    PlayTurnForm,
                    ScoreForms,
                    GameForms,
                    UserForms,
                    HistoryForms)

from utils import get_by_urlsafe, validate_input
from game_logic import (validate_guess,
                        handle_right_answer,
                        handle_wrong_answer)


USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(
                                           1, required=True),
                                           email=messages.StringField(
                                           2, required=True))
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
PLAY_TURN_REQUEST = endpoints.ResourceContainer(PlayTurnForm,
                                                urlsafe_game_key=messages.
                                                StringField(1))
SIMPLE_USER_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1))
SIMPLE_GAME_REQUEST = endpoints.ResourceContainer(
    urlsafe_game_key=messages.StringField(1))
HIGH_SCORE_REQUEST = endpoints.ResourceContainer(
    number_of_results=messages.StringField(1, default='0'))


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
                      name='create_new_game',
                      http_method='POST')
    def create_new_game_api(self, request):
        """ Create a new game. Requires an exiting user"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                'There is no user with that name!')
        try:
            history_record = [HistoryRecord(play_sequence=1,
                                            action='Game created',
                                            user_entry=" ",
                                            result=" ",
                                            current_game="",
                                            game_over=False,
                                            game_won=False,
                                            game_cancelled=False)]
            game = Game.create_new_game_models(
                user.key, request.answer, request.strikes, history_record)
            Score.create_new_score_models(user, game)
        except ValueError:
            raise endpoints.BadRequestException(
                'You really need a positive number of strikes')
        input_validation = validate_input(game.answer)
        if input_validation[0] is True:
            return game.to_form('Have fun playing Hangman!')
        else:
            raise endpoints.BadRequestException(input_validation[1])
        # The taskqueue job will go here

    @endpoints.method(request_message=PLAY_TURN_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',  # Hand populated
                      name='play_turn',
                      http_method='PUT')
    def play_turn_api(self, request):
        """ Process user input"""

        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        score = Score.query(Score.game == game.key).get()
        user = User.query(game.user == User.key).get()
        user_guess = request.guess.upper()

        """ Validate game status"""
        if game.game_over is True:
            msg = "This game is already over!"
            raise endpoints.BadRequestException(msg)

        # Validate user input
        input_validation = validate_input(request.guess, 1)

        if input_validation[0] is False:
            raise endpoints.BadRequestException(input_validation[1])
        else:
            answer_valid = validate_guess(game, user_guess)

            if answer_valid is True:
                game_state = handle_right_answer(user, game, score, user_guess)
            else:
                game_state = handle_wrong_answer(user, game, score, user_guess)

        return game_state.get('game').to_form(game_state.get('msg'))

    @endpoints.method(request_message=SIMPLE_USER_REQUEST,
                      response_message=ScoreForms,
                      path='scores/user/{user_name}',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """Returns all of a user's scores"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                'A user with that name does not exist')
        scores = Score.query(Score.user == user.key)
        return ScoreForms(items=[score.to_form() for score in scores])

    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Returns all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(request_message=SIMPLE_USER_REQUEST,
                      response_message=GameForms,
                      path='active_games/user/{user_name}',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Returns all active games for a user"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                'A user with that name does not exist')
        games = Game.query(Game.user == user.key, Game.game_over == False)
        print str(games)
        return GameForms(items=[game.to_form() for game in games])

    @endpoints.method(request_message=SIMPLE_GAME_REQUEST,
                      response_message=StringMessage,
                      path='game/cancel/{urlsafe_game_key}',
                      name='cancel_game',
                      http_method='PUT')
    def cancel_game(self, request):
        """Cancel game"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        score = Score.query(Score.game == game.key).get()
        if not game:
            raise endpoints.NotFoundException('This game does not exist')
        if game.game_cancelled is True:
            raise endpoints.BadRequestException(
                'You cannot cancel a game that is already cancelled!')
        if game.game_over is True:
            raise endpoints.BadRequestException(
                'You cannot cancel a game that is already over!')

        game.game_cancelled = True
        game.game_over = True
        game.game_won = False
        game.game_sequence += 1

        history_record = [HistoryRecord(play_sequence=game.game_sequence,
                                        action="Game cancelled",
                                        user_entry="",
                                        result="",
                                        current_game=game.current_game,
                                        game_over=game.game_over,
                                        game_won=game.game_won,
                                        game_cancelled=game.game_cancelled)]

        game.game_history += history_record

        game.put()

        score.game_over = True
        score.game_status = 'Cancelled'
        score.final_score = 0
        score.put()

        return StringMessage(
            message='Game {} cancelled!'.format(request.urlsafe_game_key))

    @endpoints.method(request_message=HIGH_SCORE_REQUEST,
                      response_message=ScoreForms,
                      path='high_scores',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """Returns a list of scores sorted by final_score in
        descending order"""
        try:
            count_of_results = int(request.number_of_results)
            if count_of_results == 0:
                scores = Score.query(Score.game_status ==
                                     'Won').order(-Score.final_score).fetch()
            else:
                scores = Score.query(
                    Score.game_status == 'Won').order(
                    -Score.final_score).fetch(limit=count_of_results)
            print scores
            return ScoreForms(items=[score.to_form() for score in scores])
        except:
            raise endpoints.BadRequestException('Numbers only please...')

    @endpoints.method(response_message=UserForms,
                      path='rankings',
                      name='get_user_rankings',
                      http_method='GET')
    def get_user_rankings(self, request):
        """Returns all users sorted by ranking"""
        users = User.query().order(-User.total_score)
        return UserForms(items=[user.to_form() for user in users])

    @endpoints.method(request_message=SIMPLE_GAME_REQUEST,
                      response_message=HistoryForms,
                      path='game/history/{urlsafe_game_key}',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Returns full history of a game"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)

        history_items = []

        for i in range(0, len(game.game_history)):
            history_items.append(game.to_history_form(i))

        return HistoryForms(items=history_items)


api = endpoints.api_server([HangmanApi])
