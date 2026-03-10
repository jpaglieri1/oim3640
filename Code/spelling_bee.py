## Re-creating the NYT spelling bee game in python
import random as rand
import pandas as pd

data = pd.read_csv("c:\Docs\Babson\OIM3640\oim3640\Data\words.csv")
word_list = data.iloc[:,0].tolist()

letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def gameplay(letters, guess):
    for i in guess:
        if i in letters:
            continue
        else:
            print("Invalid guess")
            return False
    return True

def check_guess(glist, guess):
    if guess in glist:
        print("Already guessed")
        return False
    else:
        return True

game = 1

while game != "0":
    round = 0
    gamelets = []
    for i in range(7):
        let = rand.randint(0,25)
        gamelets.append(letters[let])
    guesses = []
    score = 0
    print(gamelets)
    while round == 0:
        guess = str(input("Input guess or 0 if finished:" ))
        if guess in word_list:
            if check_guess(guesses, guess) and gameplay(gamelets, guess) == True:
                score += 1
                print("+1")
                guesses.append(guess)
        elif guess == "0":
            print("Score:", score)
            break
        else:
            print("Invalid guesses")
    game = input("Input 0 to exit: ")