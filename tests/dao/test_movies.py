import pytest
from project.dao.main import MoviesDAO
from project.models import Movie


class TestMoviesDAO:

    @pytest.fixture
    def movies_dao(self, db):
        return MoviesDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        m = Movie(
            title="Монстр в Париже",
            description="Париж. 1910 год. Ужасный монстр",
            trailer="https://www.youtube.com/watch?v=rKsdTuvrF5w",
            year=2010,
            rating=6.1,
            genre_id=16,
            director_id=18,
        )
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def movie_2(self, db):
        m = Movie(
            title="Душа",
            description="Джо становится наставником упрямой души 22",
            trailer="https://www.youtube.com/watch?v=vsb8762mE6Q",
            year=2020,
            rating=8.1,
            genre_id=16,
            director_id=16,
        )
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie_by_id(self, movies_dao, movie_1):
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert not movies_dao.get_by_id(1)

    def test_get_all_movie(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all() == [movie_1, movie_2]

    def test_get_all_movie_by_page(self, app, movies_dao, movie_1, movie_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1) == [movie_1]
        assert movies_dao.get_all(page=2) == [movie_2]
        assert movies_dao.get_all(page=3) == []

    def test_get_all_movie_by_status_new(self, app, movies_dao, movie_1, movie_2):
        app.config['ITEMS_PER_PAGE'] = 2
        status = 'new'
        assert movies_dao.get_all_movie(page=1, status=status) == [movie_2, movie_1]
