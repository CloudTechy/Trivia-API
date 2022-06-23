import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, config


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = config['test_database_name']
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            config['database_username'],
            config['database_password'],
            "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
            "question": "what is the name of the first astronaut",
            "answer": "Neil Gaiman",
            "difficulty": 5,
            "category": 5
        }
        self.bad_new_question = {
            "question": "what is the name of the first astronaut",
            "difficulty": 5,
            "category": 5
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and
    for expected errors.
    """

    def test_api_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertTrue(data['categories'])
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_api_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_error_404_api_get_questions_of_invalid_page(self):
        res = self.client().get('/questions?page=1000000000000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertTrue(data['code'])
        self.assertFalse(data['success'])

    def test_api_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertTrue(data['question'])
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_400_if_create_question_request_is_invalid(self):
        res = self.client().post("/questions", json=self.bad_new_question)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'])
        self.assertTrue(data['code'])
        self.assertEqual(res.status_code, 400)

    def test_api_get_questions_by_category(self):
        res = self.client().get('categories/1/questions?page=1')
        data = json.loads(res.data)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_error_400_api_get_questions_by_invalid_category(self):
        res = self.client().get('/categories/10000000000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['message'])
        self.assertTrue(data['code'])
        self.assertFalse(data['success'])

    def test_api_delete_question(self):
        question = Question.query.order_by(Question.id.desc()).first()
        res = self.client().delete(f"/questions/{question.id}")
        self.assertEqual(res.status_code, 200)

    def test_400_api_delete_question_error(self):
        res = self.client().delete("/questions/10000000000000000")
        self.assertEqual(res.status_code, 400)

    def test_api_search_question(self):
        res = self.client().post('/questions', json={"searchTerm": "19"})
        data = json.loads(res.data)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
    
    def test_404_retrieve_invalid_search_term(self):
        res = self.client().post("/questions/", json={"searchTerm": "zzzzzzzzzzzz"})
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'])
        self.assertTrue(data['code'])
        self.assertEqual(res.status_code, 404)

    def test_api_get_quiz_question(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": [20],
            "quiz_category": {
                "type": "Science",
                "id": "1"
            }})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_400_if_get_quiz_question_is_invalid(self):
        res = self.client().post("/questions", json={
            "previous_questions": [20]
            })
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'])
        self.assertTrue(data['code'])
        self.assertEqual(res.status_code, 400)
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
