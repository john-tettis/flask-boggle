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
    return render_template('home.html')
@app.route('/play')
def display_game_board():
    board = boggle_game.make_board()
    session['board']=board
    scores = session.get('games',[])
    scores = score_truncate(scores,5)
    print('board', file=sys.stdout)
    return render_template("boggle.html", board=board, scores=scores)

@app.route('/guess',methods=['POST'])
def register_guess():
    guess = request.json.get('guess')
    if not guess: return jsonify({'result':'empty'})

    res = boggle_game.check_valid_word(board=session['board'],word=guess)
    return jsonify({'result':res})

@app.route('/game/data', methods=['POST'])
def score_keeper():
    score = request.json['score']
    games = session.get('games',default = [])
    games.append(score)
    session['games'] = games
    
    return jsonify(games)

def score_truncate(scores,length):
    scores.sort(reverse=True)
    if len(scores)>length:
        del scores[length:]
    return scores


