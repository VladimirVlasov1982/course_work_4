from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    trailer = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    genre = relationship('Genre')
    director_id = Column(Integer, ForeignKey('directors.id'), nullable=False)
    director = relationship('Director')
    users = relationship('FavouriteMovie', back_populates='movie')


class User(models.Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String)
    surname = Column(String)
    favourite_genre = Column(Integer, ForeignKey('genres.id'))
    movies = relationship('FavouriteMovie', back_populates='user')


class FavouriteMovie(models.Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship('Movie')
    user = relationship('User')
