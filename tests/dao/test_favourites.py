import pytest

from project.dao import FavouriteDAO


class TestFavourites:

    @pytest.fixture
    def favourites_dao(self, db):
        return FavouriteDAO(db.session)

