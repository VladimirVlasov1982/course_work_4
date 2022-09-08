from project.tools import generate_password_hash, compare_password
import jwt
from flask import current_app, abort
from project.dao.main import UserDAO
from project.models import User


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def create(self, user_data: dict) -> User:
        # Добавление нового пользователя
        if not user_data:
            abort(400)
        user = self.dao.get_user(user_data.get('email'))
        if user:
            raise ValueError("Пользователь с таким email уже существует")
        user_data['password'] = generate_password_hash(user_data['password'])
        return self.dao.create(user_data)

    def get_user(self, mail: str) -> User:
        # Получение пользователя по его email
        return self.dao.get_user(mail)

    def partial_update(self, req_json: dict, token: bytes) -> User | None:
        # Обноление пользователя (имя, фамилия, предпочитаемый жанр)
        try:
            user_data = self.decode_token(token)
            user = self.dao.get_user(user_data['email'])
            if "name" in req_json:
                user.name = req_json.get('name')
            if "surname" in req_json:
                user.surname = req_json.get("surname")
            if "favourite_genre" in req_json:
                user.favourite_genre = req_json.get('favourite_genre')
            return self.dao.update(user)
        except Exception:
            return None

    def decode_token(self, token: bytes) -> User:
        # Получение данных о пользователе из токена
        data = jwt.decode(token, current_app.config.get('SECRET_KEY'),
                          algorithms=[current_app.config.get('JWT_ALGORITHM')])
        return data

    def update_password(self, old_password: str, new_password: str, token: bytes) -> User:
        # Обновление пароля
        user_data = self.decode_token(token)
        user = self.dao.get_user(user_data['email'])

        if not compare_password(user.password, old_password):
            abort(400)

        user.password = generate_password_hash(new_password)
        return self.dao.update(user)
