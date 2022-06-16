### Introduction

Trivia app is an API backed application, it is one of the projects from Udacity Full Stack Developer Nanodegree program. The application allows you to create, update, delete and get categorized and paginated questions and their answers. equally users can play games with it whereby random questions are asked and the score gets generated at the end of the game session for the player.

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
##### GET '/api/v1.0/categories'
General
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs.

Sample :  `curl -X GET http://127.0.0.1:5000/api/v1.0/categories`
```
    {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    }
```




