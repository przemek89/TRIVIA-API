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
    if categories_query is None:
      abort(404)
    else:
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
    if query_questions is None or categories_query is None:
      abort(404)
    else:
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
      else:
        abort(422)
    finally:
      db.session.close()
    return jsonify({
      'success': True,
      'deleted': question_id
       })

  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      if request.method == 'PUT':
        abort(405)
      else:
        body = request.get_json()
        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')
        question_to_be_created = Question(question=question, answer=answer, category=category, difficulty=difficulty)
        question_to_be_created.insert()
    except:
      db.session.rollback()
      abort(422)
    finally:
      db.session.close()
    return jsonify({
      'success': True
    })

  @app.route('/questions/search', methods=['POST'])
  def get_question_based_on_search():
    body = request.get_json()
    search_term = body.get('searchTerm', '')
    search_result = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    questions = [question.format() for question in search_result]
    if search_term is None:
      abort(404)
    else:
      return jsonify({
        'questions': questions
      })

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_question_for_category(category_id):
    requested_category = Category.query.get(category_id)
    questions_query = Question.query.filter(Question.category == requested_category).all()
    questions = [question.format() for question in questions_query]
    if requested_category is None:
      abort(404)
    else:
      return jsonify({
        'questions': questions,
        'totalQuestions': len(questions),
        'currentCategory': requested_category.type
      })

  @app.route('/quizzes', methods=['POST']) # implement 404, 422
  def get_questions():
    try:
      body = request.get_json()
      category = body.get('quiz_category')
      previous_question = body.get('previous_questions')
      query_questions = Question.query.filter(Question.category == category).filter(Question.id not in previous_question).all()
      if query_questions is None:
        abort(404)
      else:
        questions = [question.format() for question in query_questions]
        random_index = random.randint(1, len(questions))
    except:
      abort(422)
    return jsonify({
      'questions': questions[random_index]
    })

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found',
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed',
    }), 405

  @app.errorhandler(422)
  def unprocessable_request(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable',
    }), 422
  
  return app

    