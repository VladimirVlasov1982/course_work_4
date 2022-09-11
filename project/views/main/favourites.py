from flask import request
from flask_restx import Resource, Namespace
from project.container import favourite_service
from project.helpers.decorators import auth_required
from project.setup.api.models import movie

api = Namespace('favorites')


@api.route('/movies')
class FavoritesView(Resource):

    @auth_required
    @api.marshal_with(movie, code=200, description="OK")
    def get(self):
        """Получение фильмов пользователя из Избранного"""
        data = request.headers
        token = data.get('Authorization').split("Bearer ")[-1]
        return favourite_service.get_all_favourite_movies(token), 200


@api.route('/movies/<int:movie_id>')
class FavoriteView(Resource):

    @auth_required
    def post(self, movie_id: int):
        """Добавление фильма в избранное"""
        data = request.headers
        token = data.get('Authorization').split("Bearer ")[-1]
        favourite_service.create(movie_id=movie_id, token=token)
        return "", 201

    @auth_required
    def delete(self, movie_id: int):
        """Удаление фильма из избранного"""
        return favourite_service.delete(movie_id), 204
