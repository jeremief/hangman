import random

# ------------------------ SETTING UP MODELS -------------------------------


def display_current_game(current_game):
    display = ""
    for i in current_game:
        display += "%s " % i
    print display


# ------------------------ SETTING UP VARIABLES ---------------------------

answers = [['tree', 'clear', 'white'],
           ['python', 'javascript', 'dentist'],
           ['mississipi', 'waterloo', 'warringha']]

difficulty_level = 0
strikes_left = 0
user_input = ""
user_input_valid = 0
game_over = 0
game_cancelled = 0
won = 0
answer = ""
current_game = ""


# ----------------------- INITIALISING GAME PARAMETERS --------------------

while difficulty_level not in [1, 2, 3]:
    difficulty_level = raw_input("Please enter difficuty level 1, 2 or 3:")
    try:
        difficulty_level = int(difficulty_level)
    except:
        difficulty_level = 0

answer = random.sample(answers[difficulty_level-1], 1)[0]
answer = answer.upper()

answer_length = len(answer)


for i in range(0, answer_length):
    current_game += "_"

current_game = list(current_game)

strikes_left = 5

answer = (list(answer))

# -------------------------- PLAY GAME -------------------------------------


while current_game != answer and game_over != 1:
    display_current_game(current_game)
    print " "
    print "%i strike(s) left" % strikes_left
    print " "
    user_input = raw_input("Please enter a letter:")

    # Validate user input
    user_input_valid = 1
    user_input = user_input.upper()
    if user_input.isdigit() == True:
        print "Letters only please..."
        user_input_valid = 0
    if user_input.isalnum() == False:
        print "Letters only please..."
        user_input_valid = 0
    if len(user_input) != 1 and user_input != "CANCEL":
        print "Single character please..."
        user_input_valid = 0
    print "\n"

    # Test user input against answer
    if user_input_valid == 1:
        if user_input != "CANCEL":
            if user_input in answer:
                for i in answer:
                    if user_input == i:
                        for j in range(0, len(current_game)):
                            if answer[j] == i:
                                current_game[j] = user_input
                print "CORRECT"
                if current_game == answer:
                    won = 1
                    game_over = 1
                    display_current_game(current_game)
            else:
                print "WRONG"
                strikes_left -= 1
                print " "
                if strikes_left == 0:
                    game_over = 1
                    won = 0
        else:
            game_cancelled = 1
            game_over = 1


# --------------------------- END GAME -------------------------------------

if won == 1:
    print "YOU WON"
if won == 0 and game_cancelled == 0:
    print "YOU LOST"
else:
    print "GAME CANCELLED"
