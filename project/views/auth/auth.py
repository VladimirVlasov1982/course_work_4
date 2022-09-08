from flask_restx import Namespace
from flask_restx import Resource, abort
from flask import request
from project.setup.api.models import user

from project.container import user_service, auth_service

api = Namespace('auth')


@api.route('/register')
class RegisterView(Resource):

    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=201, description='OK')
    def post(self):
        """Создаем пользователя в системе"""
        req_json = request.json
        user_service.create(req_json)
        return "", 201


@api.route('/login')
class UserView(Resource):

    @api.response(404, 'Not Found')
    def post(self):
        """Авторизация пользователя"""
        req_json = request.json
        user_mail = req_json.get('email')
        user_password = req_json.get('password')
        if None in [user_mail, user_password]:
            return "", 404
        tokens = auth_service.generate_tokens(user_mail, user_password)
        return tokens, 201

    @api.response(404, "Not Found")
    def put(self):
        """Проверка токенов на валидность"""
        req_json = request.json
        access_token = req_json.get('access_token')
        refresh_token = req_json.get('refresh_token')
        return auth_service.approve_refresh_token(refresh_token, access_token), 204

