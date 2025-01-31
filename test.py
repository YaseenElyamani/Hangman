import random
import requests

#DONE
def get_word():
    found = False
    attempts = 0
    max_attempts = 10

    while not found and attempts < max_attempts:
        attempts += 1

        try: 
            api_url = 'https://api.api-ninjas.com/v1/randomword'
            response = requests.get(api_url, headers={'X-Api-Key': '/busKGwZsh4dMsAq3MKtww==5DiQkKoXNx9tk9Va'})
            if response.status_code == requests.codes.ok:
                response = response.json()
                word = response.get('word', '')

                if not word:  # Handle empty word response
                    continue
                response2 = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word[0]}")
                if response2.status_code == 200:
                    data = response2.json()
                    meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
                    
                    if meaning:
                        found = True
                    else:
                        continue
        except Exception as e:
            continue
    
    if not found:
        return None, None

    return word[0], meaning

#The method displays the word
def display_word(string_word):

    for v in string_word:
        print(f"{v} ", end='')
    print('')

    return string_word

#DONE
def get_attempts():

    difficulty = input("Which difficulty which you like (Easy, Medium or Hard)? ")
    attempts = 0

    while attempts == 0:
        if (difficulty.lower() == "easy"):
            attempts = 10
        elif (difficulty.lower() == "medium"):
            attempts = 6
        elif (difficulty.lower() == "hard"):
            attempts = 3
        else:
            print("Invalid input, please input Easy, Medium or Hard")
            difficulty = input("Which difficulty which you like (Easy, Medium or Hard)? ")

    return attempts

def play_game():
    #Declaration for word list and attemps
    ans = get_word()
    word = ans[0]
    definition = ans[1]
    guessed = []
    attempts = get_attempts()

    lowered_word = word.lower()
    
    string_word = '_' * len(word)
    

    print("\n==============================================================\n")
    display_word(string_word)
    print(f"\nYou have {attempts} attempts")
    print(f"{definition}\n")

    guess = input("Choose your first letter: ")

    # Loops through code as long as user has at least 1 attempt remaining
    while attempts >= 1:
        #Checks if letter has been guessed before
        if len(guess) > 1:
            if guess == lowered_word:
                print("\nCongratulations! You are the winner!")
                return
            else:
                attempts -= 1
                guessed.append(guess)
                print(f"Wrong!, attemps left {attempts}: ")
                

        if len(guess) == 1:
            if guess not in guessed:

                guessed.append(guess)

                #Checks if letter is in the word
                if guess.lower() in lowered_word:
                
                    print(f"Correct, {guess} letter is in the word")

                    #Replaces _ String with the guessed letter
                    for i in range(len(word)):
                        if word[i].lower() == guess:
                            string_word = string_word[:i] + guess + string_word[i + 1:]
                            i = 0

                    #Displays the word
                    display_word(string_word)
                
                else:
                    #If wrong letter selected, attempt is deducted
                    attempts -= 1
                    if attempts == 0:
                        break
                    print(f"Wrong letter, attemps left {attempts}: ")

            else:
                print("You have already guessed this letter!")
        

        #If you have guessed the word
        if string_word.lower() == lowered_word:
            print("\nCongratulations! You are the winner!")
            return

        guess = input("Choose your next letter: ")

    #If you lose the game and run out of attempts
    print("\nYou have lost the game, try again next time!")
    print(f"The word was {word}")

    return


def main():
    play_game()

main()
