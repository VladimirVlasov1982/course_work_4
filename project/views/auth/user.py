from flask import request
from flask_restx import Namespace, Resource
from project.container import user_service
from project.helpers.decorators import auth_required
from project.setup.api.models import user

api = Namespace('user')


@api.route('/')
class UserView(Resource):

    @auth_required
    @api.marshal_with(user, code=200, description="OK")
    def get(self):
        """Получаем профиль пользователя"""
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user_data = user_service.decode_token(token)
        mail = user_data.get('email')

        return user_service.get_user(mail), 200

    @auth_required
    @api.marshal_with(user, code=204)
    def patch(self):
        """Обновляем имя, фамилию и предпочитаемый жанр пользователя"""
        req_json = request.json
        token = request.headers['Authorization'].split("Bearer ")[-1]
        return user_service.partial_update(req_json, token), 204


@api.route('/password')
class PasswordView(Resource):

    @auth_required
    def put(self):
        """Обновляем пароль пользователя"""
        req_json = request.json
        old_password = req_json.get('old_password')
        new_password = req_json.get('new_password')
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user_service.update_password(old_password, new_password, token)
        return "", 204
