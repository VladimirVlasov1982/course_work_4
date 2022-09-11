from project.dao import GenresDAO, DirectorsDAO, MoviesDAO, UserDAO, FavouriteDAO
from project.services import GenresService, DirectorsService, MoviesService, FavouriteService
from project.services.auth_service import AuthService
from project.services.users_service import UserService
from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
director_dao = DirectorsDAO(db.session)
movie_dao = MoviesDAO(db.session)
user_dao = UserDAO(db.session)
favourite_dao = FavouriteDAO(db.session)

# Services
genre_service = GenresService(dao=genre_dao)
director_service = DirectorsService(dao=director_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UserService(dao=user_dao)
auth_service = AuthService(user_service=user_service)
favourite_service = FavouriteService(dao=favourite_dao)
