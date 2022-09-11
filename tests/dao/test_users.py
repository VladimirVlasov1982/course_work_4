import pytest
from project.dao import UserDAO
from project.models import User


class TestUserDAO:

    @pytest.fixture
    def user_dao(self, db):
        return UserDAO(db.session)

    @pytest.fixture
    def user_data(self):
        user_data = {
            "email": 'test@test.com',
            "password": "test",
            "name": "Test",
            "surname": "Testing",
            "favourite_genre": "Фантастика",
        }
        return user_data

    @pytest.fixture
    def user_1(self, db):
        user_1 = User(
            email='user_1@mail.ru',
            password='qwe123',
            name='User1',
            surname='Surname1',
            favourite_genre='Genre1',
        )
        db.session.add(user_1)
        db.session.commit()
        return user_1

    @pytest.fixture
    def user_2(self, db):
        user_2 = User(
            email='user_2@mail.ru',
            password='qwe234',
            name='User2',
            surname='Surname2',
            favourite_genre='Genre2',
        )
        db.session.add(user_2)
        db.session.commit()
        return user_2

    def test_get_all(self, user_dao, user_1, user_2):
        users = user_dao.get_all()
        assert len(users) > 0
        assert users == [user_1, user_2]

    def test_get_user(self, user_1, user_dao):
        assert user_dao.get_user(user_1.email) == user_1

    def test_create(self, user_dao, user_data):
        user = user_dao.create(user_data)
        assert user.email == 'test@test.com'
        assert user.password == 'test'
        assert user.name == 'Test'
        assert user.surname == "Testing"
        assert user.favourite_genre == "Фантастика"

    def test_get_user_not_found(self, user_dao):
        assert not user_dao.get_user(mail="test@gmail.com")

    def test_update(self, user_1, user_dao):
        user_dao.update(user_1)
