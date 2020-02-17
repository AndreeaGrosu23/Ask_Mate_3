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
        questions = data_manager.get_five_questions()
        return render_template('index.html', questions=questions)


@app.route('/add-new-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    elif request.method == 'POST':

        form_data = {
            'title': request.form['title'],
            'message' : request.form['message'],
        }

        data_manager.add_new_question(form_data)

        questions = data_manager.get_five_questions()
        return render_template('index.html', questions=questions)


@app.route('/delete-question/<question_id>')
@app.route('/delete-question')
def delete_question(question_id):
        data_manager.delete_question(question_id)
        questions = data_manager.get_five_questions()
        return render_template('index.html', questions=questions)


@app.route('/delete-answer/<answer_id>')
@app.route('/delete-answer')
def delete_answer(answer_id):
        data_manager.delete_answer(answer_id)
        questions = data_manager.get_five_questions()
        return render_template('index.html', questions=questions)


@app.route('/question/<question_id>/add-new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'GET':
        return render_template('add_answer.html')
    elif request.method == 'POST':

        form_data = {
            'question_id': int(question_id),
            'message' : request.form['message'],
        }

        data_manager.add_new_answer(form_data)

        questions = data_manager.get_five_questions()
        return render_template('index.html', questions=questions)


if __name__ == '__main__':
    app.run(host= '0.0.0.0')
