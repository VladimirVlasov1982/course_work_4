import pytest

from project.models import Movie, Genre, Director


class TestMoviesView:

    @pytest.fixture
    def movies(self, db):
        movie_1 = Movie(
            title="movie_1",
            description="description_1",
            trailer="trailer_1",
            year=2020,
            rating=8.3,
            genre_id=1,
            director_id=1,
        )
        movie_2 = Movie(
            title="movie_2",
            description="description_2",
            trailer="trailer_2",
            year=2022,
            rating=7.3,
            genre_id=2,
            director_id=2,
        )
        movies = [movie_1, movie_2]
        db.session.add_all(movies)
        db.session.commit()
        return movies

    @pytest.fixture
    def genres(self, db):
        genre_1 = Genre(name="genre1")
        genre_2 = Genre(name="genre2")
        genres = [genre_1, genre_2]
        db.session.add_all(genres)
        db.session.commit()
        return genres

    @pytest.fixture
    def directors(self, db):
        diretor_1 = Director(name="director1")
        diretor_2 = Director(name="director2")
        directors = [diretor_1, diretor_2]
        db.session.add_all(directors)
        db.session.commit()
        return directors

    def test_many(self, client, movies, genres, directors):
        response = client.get('/movies')
        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json == [{
            "id": movies[0].id,
            "title": movies[0].title,
            "description": movies[0].description,
            "trailer": movies[0].trailer,
            "year": movies[0].year,
            "rating": movies[0].rating,
            "genre": {"id": genres[0].id, "name": genres[0].name},
            "director": {"id": directors[0].id, "name": directors[0].name}
        },
            {
                "id": movies[1].id,
                "title": movies[1].title,
                "description": movies[1].description,
                "trailer": movies[1].trailer,
                "year": movies[1].year,
                "rating": movies[1].rating,
                "genre": {"id": genres[1].id, "name": genres[1].name},
                "director": {"id": directors[1].id, "name": directors[1].name}
            }
        ]

    def test_movies_page(self, client, movies):
        response = client.get('/movies/?page=1')
        assert response.status_code == 200
        assert len(response.json) == 2

        response = client.get('/movies/?page=2')
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_movies_page_status(self, client, movies, genres, directors):
        response = client.get('/movies/?status=new&page=1')
        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json == [
            {
                "id": movies[1].id,
                "title": movies[1].title,
                "description": movies[1].description,
                "trailer": movies[1].trailer,
                "year": movies[1].year,
                "rating": movies[1].rating,
                "genre": {"id": genres[1].id, "name": genres[1].name},
                "director": {"id": directors[1].id, "name": directors[1].name}
            },
            {
                "id": movies[0].id,
                "title": movies[0].title,
                "description": movies[0].description,
                "trailer": movies[0].trailer,
                "year": movies[0].year,
                "rating": movies[0].rating,
                "genre": {"id": genres[0].id, "name": genres[0].name},
                "director": {"id": directors[0].id, "name": directors[0].name}
            }
        ]

    def test_movie(self, client, movies, genres, directors):
        response = client.get('/movies/1')
        assert response.status_code == 200
        assert response.json == {
            "id": movies[0].id,
            "title": movies[0].title,
            "description": movies[0].description,
            "trailer": movies[0].trailer,
            "year": movies[0].year,
            "rating": movies[0].rating,
            "genre": {"id": genres[0].id, "name": genres[0].name},
            "director": {"id": directors[0].id, "name": directors[0].name}
        }

    def test_movie_not_found(self, client):
        response = client.get('/movies/5')
        assert response.status_code == 404