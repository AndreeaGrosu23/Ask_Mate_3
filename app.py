import data_manager
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list')
def all_questions():
    questions = data_manager.get_all_questions()
    return render_template('list.html', questions=questions)


@app.route('/search')
def search():
    phrase = request.args.get('q')
    questions = data_manager.search_in_questions(phrase)
    return render_template('search.html', questions=questions, phrase=phrase)


if __name__ == '__main__':
    app.run()
