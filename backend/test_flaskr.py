import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # create sample question


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET categories: success
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # GET categories: 404
    # GET questions: success
    # GET questions: 404
    # DELETE question: success
    # DELETE question: 404
    # DELETE question: 422
    # POST question: success
    # POST question: 405
    # POST question: 422
    # POST search: success
    # POST search: 404
    # GET question in category: success
    # GET question in category: 404
    # POST quizzes: success
    # POST quizzes: 404
    # POST quizzes: 422

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()