# Trivia App
Trivia app is an API backed application, it is one of the projects from Udacity Full Stack Developer Nanodegree program. The application allows you to create, update, delete and get categorized and paginated questions and their answers. equally users can play games with it whereby random questions are asked and the score gets generated at the end of the game session for the player.

# Guideline
The API is programmed using Python programming language and follows PEP 8 style guide

# Backend
## Prerequisite and local development
Developers using this project should Clone this repository or download its zip file, they should have node, python and pip installed on their local machines.
### Preparing your backend
navigate to the backend folder on your terminal.

 `pip install Virtualenv` #installs a virtual environment globally
 `Virtualenv venv` #creates a virtual environment
 `./venv/Scripts/activate` # activates the virtual environment
 `pip install -r requirements.txt` #installs all dependenies
 
 To run the application, run the following application
  ```
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run
  ```
  This directs our application to run the `__init__.py` file in the flaskr folder. working in development mode allows you to enable the debugger and restart the applicatiom anytime a change is made on the backend files.
  if running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).
  
  if everything work out fine, the application will be served at `http://127.0.0.1:5000/` by default and this serves as a proxy in the frontend configuration.
# Frontend

## preparing and setting up the Frontend
To get the frontend started, navigate to the frontend folder through your terminal and run the following commands.
```
npm install #installs dependencies
npm start   #starts the Trivia App
```
If the setup is right, the app will be served locally on the default http://localhost:3000. you can open it on any of your favorite browser.
# Tests
In order to run tests, navigate to the backend folder and run the following command.
```
    dropdb bookshelf_test
    createdb bookshelf_test
    psql bookshelf_test < books.psql
    python test_flaskr.py
```
Note: The first time you run the test, omit the dropdb command.
All tests are kept in the file and should be maintained as updates are made to the app functionality.
# API Reference

### Getting Started
- **Base URL:** Currently the app can only run locally, it was not hosted on any based URL. The API is hosted at the default `127.0.0.1:5000/`.
- **Authentication:** No authentication is required to access the API endpoints.

### Error Handling
The error JSON response is sent when an error occurs in the cause of using the API.  
The JSON error response contains four keys which are success, code, message and name.

##### Example:

```
{
    'success' : False,
    'code' : 404,
    'message': 'Resource not found, try accessing a valid resource',
    'name': 'Not Found'
}
```
#### Status code:
The API error codes follows the available HTTP standard status codes, the status codes to expect when there is an error are:
- `404`: This code is sent when there is no resource
- `422`: The code is sent when the App cannot process the request.
            this can occur when you specify an incorrect argument
- `405`: The code is sent when a request method is not acceptable by the endpoint.
- `500`: The code is sent when there is an error that has to do with the application, a bug
- `400`: The code is sent when the there is an error with the request.
Note: A `200` status code will be sent when there is no error
### Endpoint Library
##### GET '/categories'
General
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with two keys, categories, that contains an object of id: category_string key: value pairs and success, with its value as true

Sample :  `curl -X GET http://127.0.0.1:5000/categories`
```
  {
  "categories": {
    "1": "Science",       
    "2": "Art",
    "3": "Geography",     
    "4": "History",       
    "5": "Entertainment", 
    "6": "Sports"
  },
  "success": true
}
```

##### GET '/questions'
General
- Fetches paginated questions which are limited to only 10 questions per page by default.
- Request Arguments: None
- Returns: An object containing multiple keys such as: catgories, current_category, questions, success  and total_questions. the questions keys contains a list of object which represent the question, while the total_questions gives you the total number of questions which can help you in pagination.

Sample :  `curl -X GET http://127.0.0.1:5000/questions`
```
   {
  "categories": {
    "1": "Science",       
    "2": "Art", 
    "3": "Geography",     
    "4": "History",       
    "5": "Entertainment", 
    "6": "Sports"
  },
  "current_category": "Science",
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
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```
##### POST '/questions'
General
- This enables you to create your own questions.
- Request Arguments: the question and answer text, category, and difficulty score.
- Returns: An object with two keys, question, that contains an object of the created question and success, with its value as true

Sample :  `curl -X POST -H "Content-Type:application/json"  -d '{"question":"What is the rarest M&M color?","answer":"Brown","category":5,"difficulty":5}' http://127.0.0.1:5000/questions`
```
{
  "question": {
    "answer": "Brown",
    "category": 5,
    "difficulty": 5,
    "id": 25,
    "question": "What is the rarest M&M color?"
  },
  "success": true
}
```
##### GET '/categories/{id}/questions'
General
- Fetches a list of paginated questions under a specific category
- Request Arguments: category id passed through the url
- Returns: An object containing multiple keys such as: catgories, current_category, questions, success  and total_questions. the questions keys contains a list of object which represent the question, while the total_questions gives you the total number of questions which can help you in pagination.

Sample :  ` curl -X GET http://127.0.0.1:5000/categories/1/questions`
```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Ebuka",
      "category": 1,
      "difficulty": 5,
      "id": 24,
      "question": "who created you"
    },
    {
      "answer": "a boy",
      "category": 1,
      "difficulty": 1,
      "id": 25,
      "question": "who is obi"
    }
  ],
  "success": true,
  "total_questions": 6
}
```
##### POST '/questions' (Search)
General
- Allows you to perform a swift search operation for questions containing the giving keyword.
- Request Arguments: searchTerm string.
- Returns: An object containing multiple keys such as: catgories, current_category, questions, success  and total_questions. the questions keys contains a list of object which represent the question, while the total_questions gives you the total number of questions which can help you in pagination.

Sample :  `curl -X POST -H "Content-Type:application/json"  -d '{"searchTerm":"19"}' http://127.0.0.1:5000/questions`
```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```
##### DELETE '/questions/{id}'
General
- removes a specific question.
- Request Arguments: Question ID passsed through the url
- Returns: An object containing the id of the deleted question and success key with a true value

Sample :  `curl -X DELETE http://127.0.0.1:5000/questions/25`
```
{
  "id": 25,
  "success": true
}
```
##### POST '/quizzes'
General
- This allows users play trivia game, by answering random questions from a category if specified and the user score will be shown to the player at the end of the game.
- Request Arguments: category and previous question parameters
- Returns: An object with question key containing a random question within the given category and a success key with a true value.

Sample :  `curl -X POST -H "Content-Type:application/json"  -d '{"previous_questions": [20],"quiz_category": {"type": "Science","id": "1"}}' http://127.0.0.1:5000/quizzes`
```
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```
# License
Click [here](/LICENSE.txt) to read the agreement