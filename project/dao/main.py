from typing import Optional
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User, FavouriteMovie


class GenresDAO(BaseDAO[Genre]):
    """Класс жанров"""
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    """Класс режиссеров"""
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    """Класс фильмов"""
    __model__ = Movie

    def get_all_movie(self, status: Optional[str] = None, page: Optional[int] = None) -> list[Movie]:
        # Получить все фильмы постранично и новинки, если статус - new
        stmt: BaseQuery = self._db_session.query(Movie)
        if page and status == 'new':
            movies = self._db_session.query(Movie).order_by(Movie.year.desc())
            try:
                return movies.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UserDAO(BaseDAO[User]):
    """Класс пользователей"""
    __model__ = User

    def get_user(self, mail: str) -> User:
        # Получить пользователя по его email
        user = self._db_session.query(User).filter(User.email == mail).first()
        return user

    def create(self, user_data: dict) -> User:
        # Создать пользователя
        user = User(**user_data)
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def update(self, user: User) -> User:
        # Обновить пользователя
        self._db_session.add(user)
        self._db_session.commit()
        return user


class FavouriteDAO(BaseDAO[FavouriteMovie]):
    """Класс Избранное"""
    __model__ = FavouriteMovie

    def get_all_favourite_movies(self, user_id) -> list[Movie]:
        # Получение Избранного по id пользователя
        movies = self._db_session.query(Movie).join(FavouriteMovie).filter(FavouriteMovie.user_id == user_id).all()
        return movies

    def create_favorite(self, user_id: int, movie_id: int) -> FavouriteMovie:
        # Добавление фильма в Избранное
        favorite = FavouriteMovie(user_id=user_id, movie_id=movie_id)
        self._db_session.add(favorite)
        self._db_session.commit()
        return favorite

    def delete(self, movie_id: int) -> None:
        # Удаление фильма из Избранного
        favorite = self._db_session.query(FavouriteMovie).filter(FavouriteMovie.movie_id == movie_id).first()
        self._db_session.delete(favorite)
        self._db_session.commit()

    def get_user(self, mail: str) -> User:
        # Получение пользователя
        return self._db_session.query(User).filter(User.email == mail).first()
