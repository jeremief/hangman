import random


# class Game(object):
#     """Game variables"""


# class Player(object):
#     """Player profile"""


# ------------------------ SETTING UP VARIABLES ---------------------------

answers = [['tree', 'clear','white'], 
           ['python', 'javascript', 'dentist'], 
           ['mississipi', 'waterloo', 'warringha']]

difficulty_level = 0
strikes_left = 0
game_over = 0
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

answer = random.sample(answers[difficulty_level-1],1)[0]
answer = answer.upper()

answer_length = len(answer)


for i in range (0, answer_length):
    current_game += "_"

current_game = list(current_game)

strikes_left = 5

answer = (list(answer))

# ------------------------- START GAME -------------------------------------
print current_game
print "%i strike(s) left" % strikes_left
print " "


while current_game != answer and game_over !=1:
    user_input = raw_input("Please enter a letter:")

    if len(user_input) == 1:
        # break
        if user_input.isdigit() == False:
            if user_input.isalnum() == True:
                user_input = user_input.upper()
                if user_input in answer:
                    for i in answer:
                        if user_input == i:
                            for j in range(0,len(current_game)):
                                if answer[j] == i:
                                    current_game[j]= user_input
                                    print current_game
                                    print "%i strike(s) left" % strikes_left
                                    print " "
                                    if current_game == answer:
                                        won = 1
                else:
                    strikes_left -= 1
                    print "%i strike(s) left" % strikes_left
                    if strikes_left == 0 :
                        game_over = 1
                        won = 0


            else:
                print "Letters only please... \n"
        else:
            print "Letters only please... \n"
    else:
        print "Single character please... \n"
 
# --------------------------- END GAME -------------------------------------

if won == 1:
    print "YOU WON"       
else:
    print "YOU LOST"
