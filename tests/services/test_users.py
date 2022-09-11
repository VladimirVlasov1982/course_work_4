from unittest.mock import patch
import jwt
import pytest
from project.models import User
from project.services.users_service import UserService


class TestUserService:
    @pytest.fixture
    @patch('project.dao.UserDAO')
    def user_dao_mock(self, dao_mock):
        dao = dao_mock()
        user_1 = User(
            id=1,
            password='123',
            email="user1@mail.ru",
            name='User1',
            surname='UserSurname1',
            favourite_genre=1
        )

        dao.get_user.return_value = user_1
        dao.create.return_value = User(id=5)
        dao.update.return_value = User(name="new name", surname="new_surname", favourite_genre="new favourite genre")

        return dao

    @pytest.fixture
    def user_service(self, user_dao_mock):
        return UserService(dao=user_dao_mock)

    @pytest.fixture
    def user(self, db):
        user = User(id=1, password="password_new", email="email@mail.ru", name="test", surname="test", favourite_genre=1)
        db.session.add(user)
        db.session.commit()
        return user

    @pytest.fixture
    def token(self):
        user_data = {
            "email": "email@mail.ru",
            "password": "password_new",
        }
        token = jwt.encode(user_data, "secret_key", algorithm="HS256")
        return token

    def test_get_user(self, user_service):
        user = user_service.get_user("user1@mail.ru")
        assert user is not None
        assert user.name == 'User1'

    def test_create_user(self, user_service, app):
        user_data = {
            "email": "email@mail.ru",
            "password": "password_new",
        }
        user = user_service.create(user_data)
        assert user is not None
        assert user.id == 5

    def test_partial_update(self, user_service, token, user):
        data = {
            "name": "new name",
            "surname": "new surname",
            "favourite_genre": "new favourite genre",
        }
        user = user_service.partial_update(data, token)
        assert user is not None
        assert user.name == "new name"

