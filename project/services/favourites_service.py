import jwt
from flask import current_app
from flask_restx import abort
from project.dao import FavouriteDAO
from project.models import FavouriteMovie, Movie


class FavouriteService:
    def __init__(self, dao: FavouriteDAO):
        self.dao = dao

    def get_all_favourite_movies(self, token: bytes) -> list[Movie]:
        # Получение избранных фильмов пользователя
        user = jwt.decode(token, current_app.config.get('SECRET_KEY'),
                          algorithms=[current_app.config.get('JWT_ALGORITHM')])
        user_id = self.dao.get_user(user.get('email')).id
        movies = self.dao.get_all_favourite_movies(user_id)
        return movies

    def create(self, movie_id: int, token: bytes) -> FavouriteMovie:
        # Добавление фильма в Избранное
        user = jwt.decode(token, current_app.config.get('SECRET_KEY'),
                          algorithms=[current_app.config.get('JWT_ALGORITHM')])
        user_id = self.dao.get_user(user.get('email')).id

        return self.dao.create_favourite(user_id, movie_id)

    def delete(self, movie_id: int) -> None:
        # Удаление фильма из Избранного
        try:
            self.dao.delete(movie_id)
        except Exception:
            abort(404)
