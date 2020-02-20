import data_manager
import os
from flask import Flask,session, render_template, request, redirect, url_for

app = Flask(__name__)

app.secret_key= os.urandom(24)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('menu'))
    return render_template('first_page.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        form_data = {
            'username': request.form['username'],
            'password': data_manager.hash_password(request.form['password'])
        }
        data_manager.add_user(form_data)
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        input_pass = request.form['password']
        db_pass = data_manager.login(request.form['username'])
        if data_manager.verify_password(input_pass, db_pass['password']):
            session['username'] = request.form['username']
            return redirect(url_for('menu'))
        else:
            return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/menu')
def menu():
    questions = data_manager.get_five_questions()
    user_id = data_manager.get_user_id_by_username(session['username'])
    return render_template('index.html', questions=questions,user_id=user_id)



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
    answers = data_manager.get_question_with_answers(question_id)
    comments = data_manager.get_comment_to_question(question_id)
    question_tags = data_manager.display_tags(question_id)
    username_temp = data_manager.get_username_by_user_id(answers[0]['user_id'])
    username = username_temp['username']
    return render_template('question.html', answers=answers, question_id=int(question_id), question_tags=question_tags, comments=comments, username=username)



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
        user_id_temp = data_manager.get_user_id_by_username(session['username'])
        user_id = user_id_temp['id']
        form_data = {
            'title': request.form['title'],
            'message' : request.form['message'],
            'user_id' : user_id
        }

        data_manager.add_new_comment_to_question(form_data)

        questions = data_manager.get_five_questions()
        return render_template('index.html', questions=questions, comments=comments)


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
        username = session.get('username')
        user_id = dict(data_manager.get_user_id_by_username(username))
        form_data = {
            'question_id': int(question_id),
            'message' : request.form['message'],
            'user_id': int(user_id['id'])
        }

        data_manager.add_new_answer(form_data)

        questions = data_manager.get_five_questions()
        return render_template('index.html', questions=questions)



@app.route('/tags')
def list_tags():
    tags= data_manager.list_tags()
    return render_template('list_tags.html', tags=tags)


@app.route('/user/<user_id>')
def user_page(user_id):
    user_questions = data_manager.list_questions_by_user_id(user_id)
    user_answers = data_manager.list_answers_by_user_id(user_id)
    user_comments = data_manager.list_comments_by_user_id(user_id)
    return render_template('user_page.html',user_questions=user_questions, user_answers=user_answers, user_comments=user_comments)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'GET':
        return render_template('add_comment_to_question.html')
    elif request.method == 'POST':

        form_data = {
            'question_id': int(question_id),
            'message' : request.form['message'],
        }

        data_manager.add_new_comment_to_question(form_data)
        questions = data_manager.get_five_questions()
        return render_template('index.html', questions=questions)

@app.route('/delete-comment/<question_id>/<comment_id>')
@app.route('/delete-comment')
def delete_comment(question_id, comment_id):
        data_manager.delete_comment(question_id,comment_id)
        questions = data_manager.get_five_questions()
        return redirect('/question/'+str(question_id))


@app.route('/list-users')
def all_users():
    all_users = data_manager.get_all_users()
    return render_template('list_users.html', all_users=all_users)

@app.route('/question/<question_id>/vote_up')
def question_vote_up(question_id):
    answers = data_manager.get_question_with_answers(question_id)
    vote_number=int(answers[0]['vote_number'])+1

    data = {
        'vote_number': vote_number,
        'question_id': question_id
    }

    data_manager.update_vote(data)

    user_id = dict(data_manager.get_user_id_by_question_id(question_id))

    reputation = dict(data_manager.select_reputation(user_id['user_id']))
    reputation['reputation'] += 5

    data_rep = {
        'reputation': int(reputation['reputation']),
        'user_id': int(user_id['user_id'])
    }


    data_manager.update_reputation(data_rep)

    return redirect('/question/' + question_id)



@app.route('/question/<question_id>/vote_down')
def question_vote_down(question_id):
    answers = data_manager.get_question_with_answers(question_id)
    vote_number=int(answers[0]['vote_number'])-1

    data = {
        'vote_number': vote_number,
        'question_id': int(question_id),
    }

    data_manager.update_vote(data)
    user_id = dict(data_manager.get_user_id_by_question_id(question_id))

    reputation = dict(data_manager.select_reputation(user_id['user_id']))
    reputation['reputation'] -= 2

    data_rep = {
        'reputation': int(reputation['reputation']),
        'user_id': int(user_id['user_id'])
    }

    data_manager.update_reputation(data_rep)

    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/<answer_id>/answer-vote-up')
def answer_vote_up(answer_id, question_id):
    answer = data_manager.get_answer(answer_id)
    vote_number=int(answer['vote_number'])+1

    data = {
        'vote_number': vote_number,
        'answer_id': int(answer_id),
    }

    data_manager.update_answer_vote(data)
    user_id = dict(data_manager.get_user_id_by_question_id(question_id))

    reputation = dict(data_manager.select_reputation(user_id['user_id']))
    reputation['reputation'] += 10

    data_rep = {
        'reputation': int(reputation['reputation']),
        'user_id': int(user_id['user_id'])
    }

    data_manager.update_reputation(data_rep)

    answers = data_manager.get_question_with_answers(question_id)
    return redirect(url_for('question_details', answers=answers, question_id=question_id))


@app.route('/question/<question_id>/<answer_id>/answer-vote-down')
def answer_vote_down(answer_id, question_id):
    answer = data_manager.get_answer(answer_id)
    vote_number=int(answer['vote_number'])-1

    data = {
        'vote_number': vote_number,
        'answer_id': int(answer_id),
    }

    data_manager.update_answer_vote(data)
    user_id = dict(data_manager.get_user_id_by_question_id(question_id))

    reputation = dict(data_manager.select_reputation(user_id['user_id']))
    reputation['reputation'] -= 2

    data_rep = {
        'reputation': int(reputation['reputation']),
        'user_id': int(user_id['user_id'])
    }

    data_manager.update_reputation(data_rep)

    answers = data_manager.get_question_with_answers(question_id)
    return redirect(url_for('question_details', answers=answers, question_id=question_id))


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
