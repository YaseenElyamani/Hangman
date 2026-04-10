from flask import Flask, redirect, url_for, render_template, request, jsonify, session
from os import getenv
from dotenv import find_dotenv, load_dotenv
import requests


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
API_KEY = getenv("API_KEY")

app = Flask(__name__)

def initialize():
    ans = get_word()
    session["difficulty"] = None
    session["attempts"] = None
    session["word"] = ans[0]
    session["meaning"] = ans[1]
    session["guessed"] = []
    session["display_word"] = "_" * len(ans[0])

@app.route("/")
def index():
    initialize()    
    return render_template("index.html")

@app.route("/difficulty/<difficulty>", methods=["GET"])
def difficulty(difficulty):

    if not session["attempts"] and not session["difficulty"]:
        session["difficulty"] = difficulty
        difficulty = difficulty.lower()
        
        if difficulty == "easy":
            session["attempts"] = 8
        elif difficulty == "medium":
            session["attempts"] = 6
        else:
            session["attempts"] = 3
    
    return render_template("game.html", attempts=session["attempts"], word = session["word"], meaning = session["meaning"], display_word= " ".join(session["display_word"]), guessed = session["guessed"])

@app.route("/guess/<letter>", methods=["GET"])
def guess(letter):

    letter = letter.lower()
    word = session["word"]
    guessed = session["guessed"]
    string_word = session["display_word"]
    attempts = session["attempts"]

    if letter not in guessed:

        guessed.append(letter)

        if letter in word.lower():
            for i in range(len(word)):
                if word[i].lower() == letter:
                    string_word = string_word[:i] + letter + string_word[i + 1:]
                    i = 0
            session["display_word"] = string_word
        else:
            attempts -= 1
            session["attempts"] = attempts

        result = None
        if '_' not in session["display_word"]:
            result = "Winner"
        elif session["attempts"] <= 0:
            result = "Loser"
        
        if result:
            return render_template("result.html", result=result, word = session["word"])
            
    return redirect(url_for("difficulty", difficulty=session["difficulty"]))

@app.route("/result", methods=["POST"])
def result():
    answer = request.form.get("button_data")

    if answer == "Yes":
        return redirect(url_for("index"))

def get_word():
    found = False
    attempts = 0
    max_attempts = 10

    while not found and attempts < max_attempts:
        attempts += 1

        try: 
            api_url = 'https://api.api-ninjas.com/v1/randomword'
            response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
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

if __name__ == "__main__":
    app.run(debug=True)