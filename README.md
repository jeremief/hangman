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

Your folder should contain eleven files and one folder called "Images".

* Design.txt:
* README.md:
* api.py:
* app.yaml:
* cron.yaml:
* game_logic.py:
* game_logic_exploration.py:
* index.yaml:
* main.py:
* models.py:
* utils.py:


The "Images" folder contains the picture used on this page.



3. How to get started 
---------------------



4. Rules and scoring
--------------------
The rules of Hangman are fairly simple. You have to guess a word by proposing letters to the API. If the letter does form part of the word, it will be integrated in the solution that is progressively revieled.
If your guess is incorrect, you get a strike.
If you use all your strikes, you lose. If you guess the word without using all your strikes, you win.

The scoring is a bit complex and attempts to recognise the fact that longer words with few mistakes should obtain a better score than shorter words with no mistake. The number of points is only calculated for finished games that have been won. There are no points awarded for games have been lost, cancelled or left incomplete.

The scoring formula is based on the number of unique letters and the number of mistakes made:
(number of unique letters ^ number of unique letters) * ( 1-(number mistakes / number of unique letters))

This formula ensures that players are rewarded for playing harder games with longer words.



5. Enpoints and urls description 
--------------------------------
* create_user:
* create_new_game:
* play_turn:
* get_user_scores:
* get_scores:
* get_user_games:
* cancel_game:
* get_high_scores:
* get_user_rankings:
* get_game_history:


6. Examples
-----------




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


