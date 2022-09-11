import base64
import hashlib
import hmac
from typing import Union
from flask import current_app


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    # Получение хэша пароля
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_password(password_hash: Union[str, bytes], password: str) -> bool:
    # Проверка соответствия пароля из request паролю в БД
    decoded_digest = base64.b64decode(password_hash)
    hash_digest = base64.b64decode(generate_password_hash(password))

    return hmac.compare_digest(decoded_digest, hash_digest)
