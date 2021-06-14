# Movie Agency api

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
This project use postgresql
```

## Running the server

From within the app directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

**Authentication**
We use Auth0 service for authentication

Login url: *https://dev-puj8bf93.us.auth0.com/authorize?audience=movies-agency&response_type=token&client_id=6rxTmrLsOh2LBRluzS9kl7U2klEc4Dww&redirect_uri=https://127.0.0.1:3000/success*

These are accounts to use for testing purposes based on roles:
- Casting Assistant  
**Email: mahili8515@greenkic.com*  
**Password: mahili8515@greenkic.com*

- Casting Director  
**Email: yahipo5113@moxkid.com*  
**Password: yahipo5113@moxkid.com*

- Executive Producer  
**Email: pemex83684@gocasin.com*  
**Password: pemex83684@gocasin.com*

## Endpoints

You need to be authenticated to access thses apis. Use the retured token after successfull login
**Access Token** must be passed in header;

#### headers : authorization: Bearer token

### API URLS
**Local: localhost:5000**  
**Live: https://movies-agency.herokuapp.com/**  

### Movies Endpoints

**GET '/movies'**
- Fetches a list of movies 
- Request Arguments: {page: int} 

***Success Response:***
```json
{
    "movies": [
    {
        "id" : 1,
        "title" : "Fst & Furious",
        "release_date" : "12-04-2021",
    },
    {
        "id" : 2,
        "title" : "Blck List",
        "release_date" : "01-09-2021",
    }],
    "success": true,
    "status_code": 200
}
```

**POST '/movies'**
- Create a movie
- Request Arguments: None
- Data Params
```json
{
    "title" : "Blck List",
    "release_date" : "01-09-2021",
}
```

***Success Response:***
```json
{
    "sucess" : true,
    "movie" : 1,
    "status_code": 201
}
```


**PATCH '/movies/{id}'**
- Update a movie
- Request Arguments: None

```json
{
    "title" : "Blck List",
    "release_date" : "01-09-2021",
}
```

***Success Response:***
```json
{
    "sucess" : true,
    "movie" : 1,
    "status_code": 200
}
```

**DELETE '/movies/{id}'**
- Update a movie
- Request Arguments: None

***Success Response:***
```json
{
    "sucess" : true,
    "movie" : 1,
    "status_code": 200
}
```

### Actors Endpoints

**GET '/actors'**
- Fetches a list of actors
- Request Arguments: {page: int} 
- Returns: An object 

***Success Response:***
```json
{
    "actors": [
    {
        "id" : 1,
        "name" : "Joe Doe",
        "age" : 45,
        "gender": "M"
    },
    {
        "id" : 2,
        "name" : "Jack Leo",
        "age" : 27,
        "gender": "M"
    }],
    "success": true,
    "status_code": 200
}
```

**POST '/actors'**
- Create an actor
- Request Arguments: None
- Data Params
```json
{
    "name" : "Jack Leo",
    "age" : 27,
    "gender": "M"
}
```

***Success Response:***
```json
{
    "sucess" : true,
    "actor" : 1,
    "status_code": 201
}
```


**PATCH '/actors/{id}'**
- Update an actor
- Request Arguments: None

```json
{
    "name" : "Jack Leo",
    "age" : 30,
    "gender": "M"
}
```

***Success Response:***
```json
{
    "sucess" : true,
    "actor" : 1,
    "status_code": 200
}
```

**DELETE '/actors/{id}'**
- Update a actor
- Request Arguments: None

***Success Response:***
```json
{
    "sucess" : true,
    "actor" : 1,
    "status_code": 200
}
```


## Testing
To run the tests, run. Make sure you have right datas inside the database.  
Replace the token inside the test_app.py file by a valid one.
```
python test_app.py
```