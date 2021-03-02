from boggle import Boggle
from flask import Flask, render_template,session,request,jsonify
import sys
from flask_debugtoolbar import DebugToolbarExtension



boggle_game = Boggle()
app = Flask(__name__)
app.debug=False
app.config['SECRET_KEY'] ='124baby'
toolbar = DebugToolbarExtension(app)

@app.route('/')
def home():
    """Renders the home page template"""
    return render_template('home.html')

@app.route('/play')
def display_game_board():
    """Creates game board, passes it into the session, retrieves games played, and renders the html with a leaderboard and a game board"""
    board = boggle_game.make_board()
    session['board']=board
    scores = session.get('games',[])
    plays = len(scores)
    scores = score_truncate(scores,5)
    print('board', file=sys.stdout)
    return render_template("boggle.html", board=board, scores=scores,nplays=plays)

@app.route('/guess',methods=['POST'])
def register_guess():
    """handles a guess from axios request, returns whether or not the word is valid - ok, not-a-word, not-on-board, empty"""
    guess = request.json.get('guess')
    if not guess: return jsonify({'result':'empty'})

    res = boggle_game.check_valid_word(board=session['board'],word=guess)
    return jsonify({'result':res})

@app.route('/game/data', methods=['POST'])
def score_keeper():
    """Handles end-of-game score submission """
    score = request.json['score']
    games = session.get('games',default = [])
    games.append(score)
    session['games'] = games
    
    return jsonify(games)

def score_truncate(scores,length):
    """takes an array and a length, sorts the array highest to lowest, then truncates it to length"""
    scores.sort(reverse=True)
    if len(scores)>length:
        del scores[length:]
    return scores


