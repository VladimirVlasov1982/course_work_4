import base64
import hashlib
import hmac

import jwt
from flask import current_app, abort
from project.dao.main import UserDAO
from project.models import User



class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def create(self, user_data: dict) -> User:
        # Добавляем нового пользователя
        if not user_data:
            abort(400)
        user = self.dao.get_user(user_data.get('email'))
        if user:
            raise ValueError("Пользователь с таким email существует")
        user_data['password'] = self.genrate_hash(user_data['password'])
        return self.dao.create(user_data)

    def get_user(self, mail: str) -> User:
        return self.dao.get_user(mail)

    def partial_update(self, req_json: dict, token: bytes) -> User:
        user_data = self.decode_token(token)
        user = self.dao.get_user(user_data['email'])
        if "name" in req_json:
            user.name = req_json.get('name')
        if "surname" in req_json:
            user.surname = req_json.get("surname")
        if "favorite_genre" in req_json:
            user.favorite_genre = req_json.get('favorite_genre')
        return self.dao.update(user)

    def generate_hash(self, password: str) -> bytes:
        # Получаем хеш пароля
        hash_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            current_app.config.get("PWD_HASH_SALT"),
            current_app.config.get("PWD_HASH_ITERATIONS"),
        )
        return base64.b64encode(hash_digest)

    def compare_password(self, hash_password, password) -> bool:
        # Проверка соответствия пароля из request паролю в БД
        decoded_digest =base64.b64decode(hash_password)
        hash_digest = base64.b64decode(self.generate_hash(password))
        return hmac.compare_digest(decoded_digest, hash_digest)

    def decode_token(self, token: bytes) -> User:
        data = jwt.decode(token, current_app.config.get('SECRET_KEY'),
                          algorithms=[current_app.config.get('JWT_ALGORITHM')])
        return data

    def update_password(self, password_1: str, password_2: str, token: bytes) -> None:
        # Обновление пароля
        user_data = self.decode_token(token)
        user = self.dao.get_user(user_data['email'])
        print(user.email)
        if not self.compare_password(user.password, password_1):
            abort(400)

        user.password = self.generate_hash(password_2)
        self.dao.update(user)



