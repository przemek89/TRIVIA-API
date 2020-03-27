# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Reference

Getting Started

1. Base URL: Currently this application is only hosted locally. The backend is hosted at http://127.0.0.1:5000/
2. Authentication: This version does not require authentication or API keys.

Error Handling

The API will return 3 types of errors:
1. 404 - resource not found
2. 405 - method not allowed
3. 422 - unprocessable

Errors will be returned in the following format:
{'success': False,
'error': 405,
'message': 'method not allowed'}

List of Endpoints:
1. GET '/categories'
2. GET '/questions'
3. DELETE '/questions/<int:question_id>'
4. POST '/questions'
5. POST '/questions/search'
6. GET '/categories/<int:category_id>/questions'
7. POST '/quizzes'

GET '/categories'
- Request Arguments: None
- Returns a list of categories
- Sample:
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Request Arguments: Page number, as the results are paginated
- Returns a list of 10 questions per page, total number of questions, list of categories and current category, which is equal to None
- Sample:
    {"success": True,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }],
    "total_questions": 19,
    "currentCategory": None,
    "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
      }}

DELETE '/questions/<int:question_id>'
- Request Arguments: ID of the question, which is going to be deleted
- Returns: Confirmation if request was successfully handled and ID of the deleted question
- Sample:
{"deleted": "1",
"success": True}

POST '/questions'
- Request Arguments:
    1. Question text, which is of type String
    2. Answer text, which is of type String
    3. Category text, which is of type String
    4. Difficulty, which is of type integer
- Returns: Confirmation if request was successfully handled
- Sample:
{"success": True}

POST '/questions/search'
- Request Arguments: Search term, which is of type String
- Returns: List of all questions, which match with the search term
- Sample:
{"success": True,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }]}


GET '/categories/<int:category_id>/questions'
- Request Arguments: Category ID
- Returns:
    1. A list of all questions, which belong to the given category
    2. Total number of all returned questions
    3. Category, which was requested
- Sample:
{"success": True,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }],
    "totalQuestions": 2,
    "currentCategory": 4
        }

POST '/quizzes'
- Request Arguments:
    1. Quiz Category
    2. List of Previous Questions
- Returns: Randomly chosen question in a given category
- Sample:
{"success": True,
    "questions": [
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }}

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```