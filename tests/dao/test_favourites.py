import pytest

from project.dao import FavouriteDAO
from project.models import FavouriteMovie


class TestFavourites:

    @pytest.fixture
    def favourites_dao(self, db):
        return FavouriteDAO(db.session)

    def test_get_all_favourite_movies(self, favourites_dao, user_id=1):
        movies = favourites_dao.get_all_favourite_movies(user_id)
        assert type(movies) == list

    def test_create_favourite(self, favourites_dao):
        favourites_dao.create_favourite(user_id=1, movie_id=2)

    def test_delete(self, favourites_dao):
        favourites_dao.delete(movie_id=2)
