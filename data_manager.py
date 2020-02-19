import database_common
import bcrypt


@database_common.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                   """)
    all_questions = cursor.fetchall()
    return all_questions


@database_common.connection_handler
def get_all_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer;
                   """)
    all_answers = cursor.fetchall()
    return all_answers


@database_common.connection_handler
def search_in_questions(cursor, phrase):

    query = """
                    SELECT DISTINCT question.id AS id, question.submission_time AS submission_time , question.view_number AS view_number, question.vote_number AS vote_number, question.title AS title, question.message AS message, question.image AS image, answer.id AS a_id, answer.question_id AS a_question_id, answer.submission_time AS a_submission_time, answer.vote_number AS a_vote_number, answer.message AS a_message, answer.image AS a_image 
                    FROM question
                    LEFT JOIN answer
                    ON question.id = answer.question_id
                    WHERE question.title LIKE %(phrase)s 
                    OR question.message LIKE %(phrase)s 
                    OR answer.message LIKE %(phrase)s;
                   """
    cursor.execute(query,
                   {'phrase': '%'+phrase+'%'})
    results=cursor.fetchall()
    return results


@database_common.connection_handler
def get_question_with_answers(cursor, question_id):
    cursor.execute("""  
                    SELECT question.id AS ID, question.submission_time AS submission_time , question.view_number AS view_number, question.vote_number AS vote_number, question.title AS title, question.message AS message, question.image AS image, answer.id AS a_id, answer.question_id AS a_question_id, answer.submission_time AS a_submission_time, answer.vote_number AS a_vote_number, answer.message AS a_message, answer.image AS a_image
                    FROM question
                    LEFT JOIN answer
                    ON question.id=answer.question_id
                    WHERE question.id=%(question_id)s;
                    """,
                   {'question_id': question_id})
    question_with_answer = cursor.fetchall()
    return question_with_answer


@database_common.connection_handler
def get_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE answer.id=%(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    answer=cursor.fetchone()
    return answer


@database_common.connection_handler
def update_answer(cursor, data):
    cursor.execute("""
                    UPDATE answer
                    SET message=%s
                    WHERE  id = %s ;
                    """,
                   (data['answer_message'],
                    data['answer_id'])
                   )


@database_common.connection_handler
def get_five_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                   """)
    five_questions = cursor.fetchall()
    return five_questions

@database_common.connection_handler
def add_new_question(cursor, data):
    cursor.execute("""
                    INSERT INTO question ( submission_time, view_number, vote_number, title, message)
                    VALUES ( date_trunc('seconds', CURRENT_TIMESTAMP), 0, 0, %s, %s) ;
                   """,
                  (data['title'],
                    data['message'])
                    )


@database_common.connection_handler
def add_new_answer(cursor, data):
    cursor.execute("""
                    INSERT INTO answer ( submission_time, vote_number, question_id, message)
                    VALUES ( date_trunc('seconds', CURRENT_TIMESTAMP), 0, %s, %s) ;
                   """,
                  (data['question_id'],
                    data['message'])
                    )

@database_common.connection_handler
def add_user(cursor, data):
    cursor.execute("""
        INSERT INTO users(username, password, registration_time)
        VALUES (%s, %s,date_trunc('seconds', CURRENT_TIMESTAMP) );
    """,
                   (data['username'],
                    data['password']))

@database_common.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)

@database_common.connection_handler
def login(cursor, username):
    cursor.execute("""
        SELECT password FROM users
        WHERE username = %(username)s;
    """, {'username': username})
    password= cursor.fetchone()
    return password


@database_common.connection_handler
def display_tags(cursor, question_id):
    cursor.execute("""
        SELECT name FROM tag
        LEFT JOIN question_tag on tag.id = question_tag.tag_id
        WHERE question_tag.question_id=%(question_id)s;
                    """,
                   {'question_id': question_id})
    tags = cursor.fetchone()
    return tags['name']

@database_common.connection_handler
def list_tags(cursor):
    cursor.execute("""
        SELECT tag.name, COUNT(qt.question_id) as number_of_questions FROM tag
        LEFT JOIN question_tag qt on tag.id = qt.tag_id
        GROUP BY tag.name
    """)
    all_tags = cursor.fetchall()
    return all_tags