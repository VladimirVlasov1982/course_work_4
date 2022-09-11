import pytest
from unittest.mock import patch
from project.exceptions import ItemNotFound
from project.models import Movie
from project.services import MoviesService


class TestMoviesService:

    @pytest.fixture
    @patch('project.dao.MoviesDAO')
    def movies_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_by_id.return_value = Movie(
            id=1,
            title="test_movie",
            description="description_1",
            trailer="trailer_1",
            year=2010,
            rating=6.1,
            genre_id=16,
            director_id=18,
        )
        dao.get_all_movie.return_value = [
            Movie(
                id=1,
                title="test_movie_1",
                description="description_1",
                trailer="trailer_1",
                year=2010,
                rating=6.1,
                genre_id=16,
                director_id=18,
            ),
            Movie(
                id=2,
                title="test_movie_2",
                description="description_2",
                trailer="trailer_2",
                year=2021,
                rating=6.1,
                genre_id=16,
                director_id=18,
            )
        ]
        return dao

    @pytest.fixture
    def movies_service(self, movies_dao_mock):
        return MoviesService(dao=movies_dao_mock)

    @pytest.fixture
    def movie(self, db):
        obj = Movie(
            title="movie",
            description="description",
            trailer="trailer",
            year=2010,
            rating=6.1,
            genre_id=16,
            director_id=18,
        )
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_movie(self, movies_service, movie):
        assert movies_service.get_item(movie.id)

    def test_movie_not_found(self,movies_service, movies_dao_mock):
        movies_dao_mock.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            movies_service.get_item(10)

    @pytest.mark.parametrize('page, status', [(1, 'new'), (1, None), (None, None)],
                             ids=['with page and status', 'with page and without status', 'without page and without status'])
    def test_get_movies(self, movies_service, movies_dao_mock, page, status):
        movies = movies_service.get_all_movie(status, page)
        assert len(movies) == 2
        assert movies == movies_dao_mock.get_all_movie.return_value
        movies_dao_mock.get_all_movie.assert_called_with(status=status, page=page)

