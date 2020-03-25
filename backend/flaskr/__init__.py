import os
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

  CORS(app, resources={r"/*": {origins: '*'}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    return response

  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories_query = Category.query.all()
    categories = {}
    for category in categories_query:
      categories[category.id] = category.type
    return jsonify({
      'categories': categories
      })

  @app.route('/questions', methods=['GET'])
  def get_paginated_questions():
    # get all questions
    query_questions = Question.query.all()
    page = request.args.get('page', 1, type=int)
    begin_index = (page - 1) * 10
    end_index = begin_index + 10
    questions = [question.format() for question in query_questions]
    totalQuestions = len(questions)

    # get all categories (from Category model)
    categories_query = Category.query.all()
    categories = {}
    for category in categories_query:
      categories[category.id] = category.type

    currentCategory = None # I had a problem to understand where should I take it from, and what is it used for, I took the solution from https://knowledge.udacity.com/questions/82424

    return jsonify({
      'questions': questions[begin_index:end_index],
      'totalQuestions': totalQuestions,
      'currentCategory': currentCategory,
      'categories': categories
    })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question_to_be_deleted = Question.query.get(question_id)
      question_to_be_deleted.delete()
    except:
      db.session.rollback()
      if question_to_be_deleted is None:
        abort(404)
    finally:
      db.session.close()
    return jsonify({
      'success': True,
      'deleted': question_id
       })

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    