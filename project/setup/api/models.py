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

user: Model = api.model('Пользователь', {
    "id": fields.Integer(required=True, example=1),
    "email": fields.String(required=True, example='username@mail.ru'),
    "name": fields.String(max_length=100, example="Name"),
    "surname": fields.String(max_length=100, example="Surname"),
    "favourite_genre": fields.Nested(genre)
})

movie: Model = api.model('Фильм', {
    "id": fields.Integer(required=True, example=1),
    "title": fields.String(required=True, example="Йеллоустоун"),
    "description": fields.String(required=True, example="Владелец ранчо пытается сохранить землю своих предков."),
    "trailer": fields.String(required=True, example="https://www.youtube.com/watch?v=UKei_d0cbP4"),
    "year": fields.Integer(example=2018),
    "rating": fields.Float(example=8.6),
    "genre": fields.Nested(genre),
    "director": fields.Nested(director),
})

favourite: Model = api.model('Избранное', {
    "user_id": fields.Nested(user),
    "movie_id": fields.Nested(movie),

})
