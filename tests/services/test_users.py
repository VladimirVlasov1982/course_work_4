from unittest.mock import patch
import pytest

from project.models import User
from project.services.users_service import UserService


class TestUserService:
    @pytest.fixture
    @patch('project.dao.UserDAO')
    def user_dao_mock(self, dao_mock):
        dao = dao_mock
        user_1 = User(
            id=1,
            password='123',
            email="user1@mail.ru",
            name='User1',
            surname='UserSurname1',
            favourite_genre=1
        )
        user_2 = User(
            id=2,
            password='456',
            email="user2@mail.ru",
            name='User2',
            surname='UserSurname2',
            favourite_genre=2
        )
        user_3 = User(
            id=3,
            password='789',
            email="user3@mail.ru",
            name='User3',
            surname='UserSurname3',
            favourite_genre=3
        )

        dao.get_user.return_value = user_1
        # dao.create.return_value = User(id=5)
        return dao

    @pytest.fixture
    def user_service(self, user_dao_mock):
        return UserService(dao=user_dao_mock)

    def test_get_user(self, user_service):
        user = user_service.get_user("user1@mail.ru")
        assert user is not None
        assert user.name == 'User1'

    def test_create_user(self, user_service):
        user_data = {
            "email": "email",
            "password": "password_new",
        }
        user = user_service.create(user_data)
        # print(user)