import jwt
import pytest

from project.config import TestingConfig
from project.models import User
from project.server import create_app
from project.setup.db import db as database
from project.tools import generate_password_hash


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    database.init_app(app)
    database.drop_all()
    database.create_all()
    database.session.commit()

    yield database

    database.session.close()


@pytest.fixture
def client(app, db):
    with app.test_client() as client:
        yield client


@pytest.fixture
def token():
    user_data = {
        "email": "email@mail.ru",
        "password": "password_new",
    }
    token = jwt.encode(user_data, 'secret_key', algorithm="HS256")
    return token


@pytest.fixture
def user(db):
    user = User(id=1, password="password_new", email="email@mail.ru", name="test", surname="test",
                favourite_genre=1)
    user.password = generate_password_hash(user.password)
    db.session.add(user)
    db.session.commit()
    return user
