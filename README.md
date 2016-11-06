HANGMAN
=======

![Alt text](/images/Screenshot/Screenshot.png?raw=true "Hangman API")


1. Description
--------------
This project is part of Udacity's Full Stack Developer Nanodegree. Its purpose is to implement a Google Cloud API that enables a user to play a game of Hangman.



2. How to install
-----------------
To obtain the files in this directory, you can either fork the repository in your own directory or download a zip file to your own machine and extract it. Either way, you should have the unzipped folder on your machine to be able to run it.

You will also need to install the [Google App Engine SDK](https://cloud.google.com/appengine/downloads) that will containt a few python packages that you will need to run the API:
* protorpc
* endpoints
* webapp2

Once the directory has been downloaded, use your command line tool to navigate to the folder containing the application.

Your folder should contain eleven files and one folder called "images".

* Design.txt: a document explaining the thinking behind the decisions made for the design of this game.
* README.md: a copy of this document.
* api.py: the main api file that powers the server.
* app.yaml: ties all dependencies together for App Engine.
* cron.yaml: lists which cron routines are run and how often they are. 
* game_logic.py: powers the play_turn api endpoint
* game_logic_exploration.py: a self-contained python exploration of the game. You can play it using the command line.
* index.yaml: file keeping track of indexes for App Engine
* main.py: defines handlers for requests to urls. In our case, it hadles the email reminders triggered by the cron file.
* models.py: contains the class definition of all custom objects used in the game
* utils.py: contains a couple of methods that help run the game without really being part of its actual logic


The "images" folder contains the picture used on this page.



3. How to get started 
---------------------
#### Running locally
You can use Google's API Explorer to play the game on localhost. You will still need an internet connection for the API explorer to work though.

Once you have installed the SDK and the Google App Engine Laucher, open the latter.
Click on File then on Add an exisitng application. Browse to the folder that contains the game files
Once you application appears in your list of applications, highlight Hangman and press the Run button.
Once it is running, press the Browse button and it will open a session in your browser.
Add "/_ah/api/explorer" at the end of the url to use the api explorer. You may need to authorise "unsafe scripts" in your browser as the API explorer doesn't like applications not starting from https, which tends to be the case for localhost instances.

Once you have been through all this, you can now use the api explorer and create users, games and play Hangman:

* Use the create_user endpoint to create a new user. Take note of the user name.
* Use the create_game endpoint to create a new game. Enter the game's answer, the number of allowed strikes and the user name you created earlier. Take note of the urlsafe key generated.
* Use the play_turn api to play the game. Enter the urlsafe key you copied from the previous step and enter your guess. Good luck!

#### Running online
Having installed all the Google elements mentioned above, you can create a projet in Google cloud and use its ID in place of the one provided here.
Once you are ready, click the Deploy button. When the application is done deploying, you can go to your url and follow the same procedure to use the api explorer.



4. Rules and scoring
--------------------
The rules of Hangman are fairly simple. You have to guess a word by proposing letters to the API. If the letter does form part of the word, it will be integrated in the solution that is progressively revealed.
If your guess is incorrect, you get a strike.
If you use all your strikes, you lose. If you guess the word without using all your strikes, you win.

The scoring is a bit complex and attempts to recognise the fact that longer words with few mistakes should obtain a better score than shorter words with no mistake. The number of points is only calculated for finished games that have been won. There are no points awarded for games have been lost, cancelled or left incomplete.

The scoring formula is based on the number of unique letters and the number of mistakes made:
(number of unique letters ^ number of unique letters) * ( 1-(number mistakes / number of unique letters))

This formula ensures that players are rewarded for playing harder games with longer words.

Players are then ranked in descending order of their score.



5. Endpoints, models, forms and urls description 
------------------------------------------------
#### Endpoints
* create_user: takes a username and email to create a unique user
  - Path: 'user'
  - Method: POST
  - Parameters: user_name, email
  - Returns: A sting confirming that the user has been created
  - Description: creates a user and returns a message confiming the user's creation

* create_new_game: takes an existing user name as well as an answer and a number of strikes to create a new game
  - Path: 'game'
  - Method: POST
  - Parameters: user_name, answer, strikes
  - Returns: A GameForm message
  - Description: creates a game and returns a GameForm message with the gam's initial state

* play_turn: 
  - Path: 'game/{urlsafe_game_key}'
  - Method: PUT
  - Parameters: urlsafe game key, guess
  - Returns: A GameForm with the current game state
  - Description: takes a urlsafe game key and a guess to play a round of Hangman. This is effectively the main component of the game.

* get_user_scores: 
  - Path: scores/user/{user_name}'
  - Method: GET
  - Parameters: user_name
  - Returns: a list of ScoreForms containing a player's scores
  - Description: returns all scores for an existing user.

* get_scores: returns all scores for all users
  - Path: 'scores'
  - Method: GET
  - Parameters: None
  - Returns: a list of ScoreForms containing all players' scores
  - Description: returns all scores for an existing user.

* get_user_games: returns all _active_ games for a user
  - Path: 'active_games/user/{user_name}''
  - Method: GET
  - Parameters: user_name
  - Returns: a list of GameForms all active games for a user 
  - Description: returns all active games for a user 

* cancel_game: 
  - Path: 'game/cancel/{urlsafe_game_key}'
  - Method: GET
  - Parameters: urlsafe game key
  - Returns: A sting confirming that the game has been cancelled
  - Description: takes a urlsafe game key to cancel the game attached to it. Cancelled games are retained in the datastore but cannot be altered anynore.

* get_high_scores: 
  - Path: 'high_scores'
  - Method: GET
  - Parameters: None, number of scores (optional)
  - Returns: a list of scores in descending order
  - Description: returns all scores in descending order. It also take an optional parameter to limit the number of recoords returned.

* get_user_rankings: returns a list of all users sorted by their score
  - Path: 'ranking'
  - Method: GET
  - Parameters: None
  - Returns: a list of UserForms sorted by socre descending order
  - Description: returns a list of all users sorted by their score

* get_game_history: 
  - Path: 'game/history/{urlsafe_game_key}'
  - Method: GET
  - Parameters: urlsafe game key
  - Returns: a list of HistoryForms containing the detailed history of each game
  - Description: takes a urlsafe game key to return a history of all turns played in a game


#### Models:
* User: stores unique user_name, email address and final score.
    
* Game: stores unique game states. Associated with User model via KeyProperty.
    
* HistoryRecord: records the results at the end of each turn played. It is a structured property of a Game.

* Score: records completed games. Associated with Users model via KeyProperty.
    

#### Forms:
* StringMessage : general purpose String container.

* UserForm: representation of a user (name, email, total_score)

* UserForms: multiple UserForm container.

* NewGameForm: used to create a new game (user_name, answer, strikes (defaults to five if not provided))

* GameForm: representation of a Game's state (urlsafe_key, strikes, mistakes, game_over, game_won, game_cancelled, message, user_name).

* GameForms: multiple GameForm container.

* PlayTurnForm: inbound make move form (guess)

* ScoreForm: representation of a completed game's Score (user_name, urlsafe_key, unique_letters, mistakes_made, game_over, game_status, final_score).

* ScoreForms: multiple ScoreForm container.

* HistoryForm: stores all they key variables in their state after a turn has been played (sequence, action, user_entry, result, current_game, game_over, game_won, game,cancelled)  

* HistoryForms: multiple HistoryForm conatiner.


#### Urls
* /crons/send_reminder: activates the cron file



6. Future projects
------------------
* Add a random game generation endpoint
* Get the reminder email to actually list the incomplete games
* Refactoring models.py into a python package



7. Licence
----------
MIT License

Copyright (c) 2016 Jeremie Faye

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



8. About
---------
Created by Jeremie Faye using code and material learned during Udacity's Full Stack Developer Nanodegree


