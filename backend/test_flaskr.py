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
        self.assertTrue(data['categories'], True)

    # GET questions: success
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'], True)
        self.assertTrue(data['totalQuestions'], True)
        self.assertTrue(data['currentCategory'], None)
        self.assertTrue(data['categories'], True)

    # GET questions: 404
    def test_get_questions_404_error(self):
        res = self.client().get('/questions?page=666')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # DELETE question: success
    def test_delete_question(self):
        # create a new question
        question = Question(question='question', answer='answer', category='category', difficulty=1)
        question.insert()

        # delete the question
        q_id = question.id
        res = self.client().delete(f'/questions/{q_id}')
        data = json.loads(res.data)

        # check if it was deleted
        deleted_question = Question.query.filter(Question.id == q_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], q_id)
        self.assertEqual(deleted_question, None)

    # DELETE question: 404
    def test_delete_question_404_error(self):
        res = self.client().delete('/questions/1234567890')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # POST question: success
    def test_post_question(self):
        # create and post a new question
        question = Question(question='question', answer='answer', category='category', difficulty=1)
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # query the new question
        posted_question = Question.query.filter(Question.category == 'category').one_or_none()
        self.assertEqual(question.question, posted_question.question)
        self.assertEqual(question.answer, posted_question.answer)
        self.assertEqual(question.category, posted_question.category)
        self.assertEqual(question.difficulty, posted_question.difficulty)

    # POST question: 405
    def test_put_question(self):
        # create and put a new question
        question = Question(question='question', answer='answer', category='category', difficulty=1)
        res = self.client().put('/questions', json=question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # POST question: 422
    def test_unprocessable_question(self):
        # create a question in a wrong format
        question = Question(question='Is it correct?', answer=True, category=123, difficulty='very hard')
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # POST search: success
    def test_post_search_questions(self):
        search_term='que'
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'], True)

    # POST search: 404
    def test_post_none_search(self):
        search_term=None
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # GET question in category: success
    def test_get_questions_in_category(self):
        # create a new question in a category
        question = Question(question='question', answer='answer', category='category', difficulty=1)
        question.insert()
        created_category = Category.query.filter(Category.type == question.category).one_or_none()
        category_id = created_category.id
        # GET the questions
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'], True)
        self.assertTrue(data['totalQuestions'], True)
        self.assertEqual(data['currentCategory'], 'category')

    # GET question in category: 404
    def test_get_questions_in_not_existing_category(self):
        res = self.client().get('/categories/878964653168465132186545613189654131685413/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # POST quizzes: success
    # POST quizzes: 404
    # POST quizzes: 422

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()