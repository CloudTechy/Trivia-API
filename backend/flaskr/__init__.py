from ast import In
from calendar import c
import os
from sys import exc_info
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    def paginate_questions(request, selections):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selections]
        return questions[start:end]
    """
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {'origins': '*'}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        result = Category.query.all()
        categories = {
            category.format()['id']: category.format()['type']
            for category in result}
        return jsonify({
            'success': True,
            'categories': categories
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and
    pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        result = Question.query.all()
        questions = paginate_questions(request, result)
        if len(questions) == 0:
            abort(404)
        result2 = Category.query.all()
        categories = {
            category.format()['id']: category.format()['type']
            for category in result2}
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions':  len(result),
            'current_category': categories[1],
            'categories': categories
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify(
                {
                    "success": True,
                    "id": question_id,
                }
            )
        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and
    the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            requestJson = request.get_json()
            if 'searchTerm' in requestJson:
                # this is a search question request implementation
                searchTerm = requestJson['searchTerm']
                result = Question.query.filter(
                    Question.question.ilike(f'%{searchTerm}%')).all()
                questions = paginate_questions(request, result)
                if len(questions) == 0:
                    abort(404)
                else:
                    result2 = Category.query.all()
                    return jsonify({
                        'success': True,
                        'questions': questions,
                        'total_questions':  len(result),
                        'current_category': result2[0].type,
                    })
            else:
                question = Question(**requestJson)
                question.insert()
                return jsonify({
                    "success": True,
                    "question":  question.format()
                })
        except:
            abort(400)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    # implemented on @app.route('/questions', methods=['POST'])
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(400)
        questions = paginate_questions(request, category.questions)
        if len(questions) == 0:
            abort(404)
        result2 = Category.query.all()
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions':  len(result2),
            'current_category': result2[0].type,
        })
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        try:
            question = None
            requestJson = request.get_json()
            previous_questions = requestJson['previous_questions']
            quiz_category = requestJson['quiz_category']
            if quiz_category['id'] != 0:
                isQuizByCategory = True
                questionsCountByCategory = Question.query.filter(
                    Question.category == quiz_category['id']).count()
            else:
                isQuizByCategory = False
            questionsCount = Question.query.count()
            randNums = []
            while (question is None) and (questionsCountByCategory !=
                                          len(previous_questions)):
                startCount = Question.query.first().id
                randNum = random.randint(
                    Question.query.first().id, questionsCount + startCount)
                if randNum in randNums or randNum in previous_questions:
                    continue
                else:
                    if isQuizByCategory:
                        result = Question.query.filter(
                            Question.category == quiz_category['id'],
                            Question.id == randNum).one_or_none()
                        if result is None:
                            randNums.append(randNum)
                        else:
                            question = result.format()
                    else:
                        result = Question.query.get(randNum)
                        if result is None:
                            randNums.append(randNum)
                        else:
                            question = result.format()
            return jsonify({
                'success': True,
                'question': question
            })
        except:
            abort(400)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def err_resource_not_found(err):
        return jsonify(
            {
                "code": err.code,
                "name": err.name,
                'success': False,
                'message': err.description
            }
        ), 404

    @app.errorhandler(400)
    def err_bad_request(err):
        return jsonify(
            {
                "code": err.code,
                "name": err.name,
                'success': False,
                'message': err.description
            }
        ), 400

    @app.errorhandler(422)
    def err_unprocessable_request(err):
        return jsonify(
            {
                "code": err.code,
                "name": err.name,
                'success': False,
                'message': err.description
            }
        ), 422

    @app.errorhandler(405)
    def err_method_not_allowed(err):
        return jsonify(
            {
                "code": err.code,
                "name": err.name,
                'success': False,
                'message': err.description
            }
        ), 405

    @app.errorhandler(500)
    def err_server_error(err):
        return jsonify(
            {
                "code": err.code,
                "name": err.name,
                'success': False,
                'message': err.description
            }
        ), 500
    return app
