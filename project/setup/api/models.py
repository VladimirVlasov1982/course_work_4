from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example="Режиссер")
})

movie: Model = api.model('Фильм', {
    "id": fields.Integer(required=True, example=1),
    "title": fields.String(required=True),
    "description": fields.String(required=True),
    "trailer": fields.String(required=True),
    "year": fields.Integer(),
    "rating": fields.Float(),
    "genre_id": fields.Integer(),
    "director_id": fields.Integer
})

user: Model = api.model('Пользователь', {
    "id": fields.Integer(required=True, example=1),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "name": fields.String(),
    "surname": fields.String(),
    "favorite_genre": fields.String(),
})
