import data_manager
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list', methods=['GET', 'POST'])
def all_questions():
    if request.method == 'GET':
        questions = data_manager.get_all_questions()
    elif request.method == 'POST':
        phrase = request.form['search']
        questions = data_manager.search_in_questions(phrase)
    return render_template('list.html', questions=questions)


if __name__ == '__main__':
    app.run()
