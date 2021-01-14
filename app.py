from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = '456-23-54'

boggle_game = Boggle()

guessed_words = []


@app.route('/start')
def start():
    board = boggle_game.make_board()
    session['board'] = board
    guessed_words.clear()

    return render_template('start.html', board=board)


@app.route('/handle-score', methods=["POST"])
def handle_score():
    session['guessed_words'] = guessed_words
    result = request.json['result']
    word = request.json['word']
    if result == 'ok' and word not in session['guessed_words']:
        guessed_words.append(word)
        try:
            session['score'] = session['score'] + len(word)
        except Exception:
            session['score'] = len(word)
    elif not len(guessed_words):
        session['score'] = 0

    try:
        session['highest_score'] = (
            max(session['score'], session['highest_score'])
        )
    except Exception:
        session['highest_score'] = session['score']

    return jsonify(
        {
            'score': session['score'],
            'word': word,
            'guessed_words': guessed_words,
        }
    )


@app.route('/check-word', methods=["POST", "GET"])
def check_word():
    word = request.json['word']
    is_valid_word = boggle_game.check_valid_word(session['board'], word)

    return jsonify({'result': is_valid_word, 'word': word})
