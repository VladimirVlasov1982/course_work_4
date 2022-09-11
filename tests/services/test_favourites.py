from unittest.mock import patch

import jwt
import pytest

from project.models import FavouriteMovie
from project.services import FavouriteService


class TestFavouriteService:

    @pytest.fixture
    @patch('project.dao.FavouriteDAO')
    def favourite_dao_mock(self, dao_mock):
        dao = dao_mock()
        favourite_1 = FavouriteMovie(id=1, user_id=1, movie_id=1)
        favourite_2 = FavouriteMovie(id=2, user_id=1, movie_id=2)
        dao.get_all_favourite_movies.return_value = [favourite_1, favourite_2]
        dao.create_favourite.return_value = FavouriteMovie(id=4, user_id=1, movie_id=3)
        dao.delete.return_value = None
        return dao

    @pytest.fixture
    def favourite_service(self, favourite_dao_mock):
        return FavouriteService(dao=favourite_dao_mock)

    @pytest.fixture
    def token(self):
        user_data = {
            "email": "email@mail.ru",
            "password": "password_new",
        }
        token = jwt.encode(user_data, 'secret_key', algorithm="HS256")
        return token

    def test_get_all_favourite_movies(self, favourite_service, token, app):
        favourites = favourite_service.get_all_favourite_movies(token)
        print(favourites)
        assert len(favourites) == 2
        assert type(favourites) == list

    def test_create(self, favourite_service, token, app, movie_id=1):
        favourite = favourite_service.create(movie_id=movie_id, token=token)
        assert favourite.id is not None

    def test_delete(self, favourite_service, movie_id=1):
        favourite_service.delete(movie_id=movie_id)
