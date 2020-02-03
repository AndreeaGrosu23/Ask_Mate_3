import database_common

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
                    SELECT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image 
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

