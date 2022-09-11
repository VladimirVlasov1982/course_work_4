import calendar
import datetime
import jwt
import pytest

from project.models import User


class TestAuthView:
    @pytest.fixture
    def generate_tokens(self, user: User) -> dict[str, str | int]:
        data = {
            "name": user.name,
            "surname": user.surname,
            "favourite_genre": user.favourite_genre,
            "email": user.email,
        }

        min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        data['exp'] = calendar.timegm(min15.timetuple())
        access_token = jwt.encode(data, 'secret_key', algorithm="HS256")

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, 'secret_key', algorithm="HS256")

        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

    @pytest.fixture
    def data(self):
        return {"email": "email@mail.ru", "password": "password_new"}

    def test_create_user(self, client, data):
        response = client.post('/auth/register', json=data)
        assert response.status_code == 201

    def test_authorization_user(self, client, data, user):
        response = client.post('/auth/login', json=data)
        assert response.status_code == 201

    def test_user_not_found(self, client, data):
        response = client.post('/auth/login', json=data)
        assert response.status_code == 404

    def test_refresh_tokens(self, client, generate_tokens):
        response = client.put('/auth/login', json=generate_tokens)
        assert response.status_code == 204

    def test_bad_request(self, client):
        response = client.put('/auth/login')
        assert response.status_code == 400
