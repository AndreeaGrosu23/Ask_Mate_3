import data_manager
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    questions = data_manager.get_five_questions()
    return render_template('index.html', questions=questions)


@app.route('/list')
def all_questions():
    questions = data_manager.get_all_questions()
    return render_template('list.html', questions=questions)


@app.route('/search')
def search():
    phrase = request.args.get('q')
    questions = data_manager.search_in_questions(phrase)
    return render_template('search.html', questions=questions, phrase=phrase)

@app.route('/question/<question_id>')
def question_details(question_id):
    answers= data_manager.get_question_with_answers(question_id)
    return render_template('question.html', answers=answers, question_id=question_id)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
@app.route('/answer')
def edit_answer(answer_id):
    if request.method== 'GET':
        answer=data_manager.get_answer(answer_id)
        return render_template('answer.html', answer=answer, answer_id=answer_id)
    elif request.method == 'POST':
        form_data = {
            'answer_id': int(answer_id),
            'answer_message': request.form['answer_message']
        }
        data_manager.update_answer(form_data)
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
