from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import os

if os.environ['FLASK_ENV'] == 'production':
    database_path = os.environ['DATABASE_URL']
    if database_path.startswith("postgres://"):
        database_path = database_path.replace(
            "postgres://", "postgresql://", 1)
else:
    database_name = "casting_agency_db"
    database_path = "postgresql://{}:{}@{}/{}".format(
        'postgres', 'noelle', 'localhost:5432', database_name)


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Many to many relationship beetween movies and actors
'''
actor_movie = db.Table('actor_movie', db.Model.metadata,
                       db.Column('movie_id', db.Integer,
                                 db.ForeignKey('movies.id')),
                       db.Column('actor_id', db.Integer,
                                 db.ForeignKey('actors.id'))
                       )

'''
Movie
'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    release_date = Column(String)
    actors = db.relationship(
        "Actor",
        secondary=actor_movie,
        back_populates="movies")

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }


'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    age = Column(Integer)
    gender = Column(String)
    movies = db.relationship(
        "Movie",
        secondary=actor_movie,
        back_populates="actors")

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
