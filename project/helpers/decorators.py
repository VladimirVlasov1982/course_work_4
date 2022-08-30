from functools import wraps
from typing import Callable

import jwt
from flask_restx import abort
from flask import request, current_app


def auth_required(func: Callable) -> Callable:
    # Декоратор для ограничения доступа на чтение
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers
        token = data.get("Authorization").split('Bearer ')[-1]
        try:
            jwt.decode(token, current_app.config.get('SECRET_KEY'),
                       algorithms=[current_app.config.get('JWT_ALGORITHM')])
        except Exception as e:
            print("JWT Decode Error", e)
            abort(401)
        return func(*args, **kwargs)
    return wrapper
