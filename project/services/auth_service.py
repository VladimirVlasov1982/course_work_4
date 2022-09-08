import calendar
import datetime

import jwt
from project.tools import compare_password
from project.services.users_service import UserService
from flask_restx import abort
from flask import current_app


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, mail: str, password: str, is_refresh=False) -> dict[str, str | int]:
        # Генерация токена
        user = self.user_service.get_user(mail)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not compare_password(user.password, password):
                abort(400)

        data = {
            "name": user.name,
            "surname": user.surname,
            "favourite_genre": user.favourite_genre,
            "email": user.email,
        }

        min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config.get('TOKEN_EXPIRE_MINUTES'))
        data['exp'] = calendar.timegm(min15.timetuple())
        access_token = jwt.encode(data, current_app.config.get('SECRET_KEY'),
                                  algorithm=current_app.config.get('JWT_ALGORITHM'))

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config.get('TOKEN_EXPIRE_DAYS'))
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, current_app.config.get('SECRET_KEY'),
                                   algorithm=current_app.config.get('JWT_ALGORITHM'))

        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

    def check_token(self, token: bytes) -> bool:
        # Проверяем токен на валидность
        try:
            jwt.decode(token, current_app.config.get('SECRET_KEY'),
                       algorithms=[current_app.config.get('JWT_ALGORITHM')])
            return True
        except Exception:
            return False

    def approve_refresh_token(self, refresh_token: bytes, access_token: bytes) -> dict[str, str | int]:
        # Генерируем access_token и refresh_token
        if not self.check_token(refresh_token) and self.check_token(access_token):
            abort(400)

        data = jwt.decode(refresh_token, current_app.config.get('SECRET_KEY'),
                          algorithms=[current_app.config.get('JWT_ALGORITHM')])

        mail = data.get('email')
        return self.generate_tokens(mail, None, is_refresh=True)
