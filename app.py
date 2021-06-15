import os
from flask import (
    Flask,
    request,
    jsonify,
    abort
)
from flask_cors import CORS
from flask_migrate import Migrate
from auth.auth import AuthError, requires_auth
from models import setup_db, db, Actor, Movie

ITEMS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    Migrate(app, db)
    CORS(app)

    '''
    @TODO: Decorator to set Access-Control-Allow
    '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def paginate(request, list):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions = [item.format() for item in list]
        return questions[start:end]

    '''
    Index
    '''
    @app.route('/')
    def index():
        return jsonify({
            'message': "Welcome to my movies agency api",
        }), 200

    '''
    Get movies
    '''
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        movies_list = paginate(request, movies)

        if(len(movies_list) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies_list,
        }), 200

    '''
    Get movie by Id
    '''
    @app.route('/movies/<int:movie_id>')
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):
        if movie_id is None:
            abort(400)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

    '''
    Create movie
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movie(payload):
        json_data = request.get_json()

        title = json_data.get("title")
        release_date = json_data.get("release_date")

        if title is None or release_date is None:
            abort(400)

        try:
            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()

            return jsonify({
                'success': True,
                'created': new_movie.id
            }), 201
        except Exception:
            abort(422)

    '''
    Delete a movie
    '''
    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        if movie_id is None:
            abort(400)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        movie.delete()
        return jsonify({
            'success': True,
            'movie': movie.id
        }), 200

    '''
    Update a movie
    '''
    @app.route('/movies/<int:movie_id>', methods=["PATCH"])
    @requires_auth('update:movies')
    def update_movie(payload, movie_id):
        if movie_id is None:
            abort(400)

        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            body = request.get_json()
            if 'title' in body:
                movie.title = body.get('title')
            if 'release_date' in body:
                movie.release_date = body.get('release_date')

            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.id
            }), 200
        except Exception:
            abort(422)

    '''
    Get actors
    '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        actors_list = paginate(request, actors)

        if(len(actors_list) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'actors': actors_list,
        }), 200

    '''
    Create actor
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_actor(payload):
        json_data = request.get_json()

        name = json_data.get("name")
        age = json_data.get("age")
        gender = json_data.get("gender")

        if name is None or age is None or gender is None:
            abort(400)

        try:
            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()

            return jsonify({
                'success': True,
                'created': new_actor.id
            }), 201
        except Exception:
            abort(422)

    '''
    Delete an actor
    '''
    @app.route('/actors/<int:actor_id>', methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        if actor_id is None:
            abort(400)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        actor.delete()
        return jsonify({
            'success': True,
            'actor': actor.id
        }), 200

    '''
    Update a actor
    '''
    @app.route('/actors/<int:actor_id>', methods=["PATCH"])
    @requires_auth('update:actors')
    def update_actor(payload, actor_id):
        if actor_id is None:
            abort(400)

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)

            body = request.get_json()
            if 'name' in body:
                actor.name = body.get('name')
            if 'age' in body:
                actor.age = body.get('age')
            if 'gender' in body:
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.id
            }), 200
        except Exception:
            abort(422)

    '''
    Create error handlers for all expected errors
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'Unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad request'
        }), 400

    @app.errorhandler(405)
    def not_allow(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method not allowed'
        }), 405

    '''
      error handler should conform to general task above
    '''
    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(500)
    def not_allow(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Server Error'
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
