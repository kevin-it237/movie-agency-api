import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

# replace value by a valid token
token = '@TOKEN'


class MovieAgencyTestCase(unittest.TestCase):
    """This class represents the movie agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        self.database_name = "casting_agency_test_db"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'noelle', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    Test for movies apis
    """

    def test_create_movies(self):
        res = self.client.post('/movies',
                               json={'title': 'Black list',
                                     'release_date': '12-04-2022'},
                               content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_400_create_movies(self):
        res = self.client.post('/movies',
                               json={},
                               content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_get_movies(self):
        res = self.client.get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_404_get_movies(self):
        res = self.client.get('/movies?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_update_movies(self):
        res = self.client.patch('/movies/8',
                                data=json.dumps(dict(title='Barby')),
                                content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_422_update_movies(self):
        res = self.client.patch('/movies/10000',
                                data=json.dumps(dict(title='Barby')),
                                content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_delete_movies(self):
        res = self.client.delete('/movies/7')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_delete_movies(self):
        res = self.client.delete('/movies/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    """
    Test for actors apis
    """

    def test_create_actors(self):
        res = self.client.post('/actors',
                               json={'name': 'John Wick',
                                     'age': 50, 'gender': "M"},
                               content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_400_create_actors(self):
        res = self.client.post('/actors',
                               json={},
                               content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_get_actors(self):
        res = self.client.get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_404_get_actors(self):
        res = self.client.get('/actors?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_update_actors(self):
        res = self.client.patch('/actors/4',
                                data=json.dumps(dict(name='Johny Jones')),
                                content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_422_update_actors(self):
        res = self.client.patch('/actors/10000',
                                data=json.dumps(dict(name='Brad Pitt')),
                                content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_delete_actors(self):
        res = self.client.delete('/actors/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_delete_actors(self):
        res = self.client.delete('/actors/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    """
    Test Casting Assistant  role
    """

    def test_401_unauthorized_update_movie(self):
        res = self.client.patch('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_401_invalid_token(self):
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer '
        res = self.client.get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    """
    Test Casting Director role
    """

    def test_401_unauthorized_delete_movie(self):
        res = self.client.delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_401_invalid_token_director_role(self):
        self.client.environ_base['HTTP_AUTHORIZATION'] = ''
        res = self.client.get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    """
    Test Executive Producer role
    """

    def test_200_executive_create_movie(self):
        res = self.client.post('/movies',
                               json={},
                               content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_401_invalid_token_executive_role(self):
        self.client.environ_base['HTTP_AUTHORIZATION'] = 'eyeadfdf'
        res = self.client.get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
