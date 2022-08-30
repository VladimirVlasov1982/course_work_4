from typing import Optional

from flask_sqlalchemy import BaseQuery
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre

class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director

class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie
    def __init__(self, db_session):
        super().__init__(db_session)
        self._db_session = db_session

    def get_all(self, status: str, page: Optional[int] = None) -> list[Movie]:
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

class UserDAO:
    def __init__(self, db_session):
        self._db_session = db_session

    def create(self, user_data: dict) -> User:
        user = User(**user_data)
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def get_user(self, mail: str) -> User:
        user = self._db_session.query(User).filter(User.email == mail).first()
        return user

    def update(self, user: User) -> User:
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def update_password(self, old_password, username):
        pass

