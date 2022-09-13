import base64

import jwt
from flask_restx import Namespace
from flask_restx import Resource
from flask import request, current_app
from project.container import user_service, auth_service
from project.setup.api.parsers import auth_parser, token_parser
from project.setup.api.models import tokens

api = Namespace('auth')


@api.route('/register')
class RegisterView(Resource):

    @api.expect(auth_parser)
    @api.response(code=201, description='Created', headers={'Location': 'The URL of a new user'})
    @api.response(code=400, description='Bad request')
    @api.response(code=409, description='Record allready exists')
    def post(self):
        """Создаем пользователя в системе"""
        user_service.create(auth_parser.parse_args())
        return "", 201


@api.route('/login')
class UserView(Resource):

    @api.expect(auth_parser)
    @api.marshal_with(tokens, code=201, description='OK')
    @api.response(code=400, description='Bad Request')
    @api.response(code=404, description='Not Found')
    def post(self):
        """Авторизация пользователя"""
        return auth_service.generate_tokens(**auth_parser.parse_args())

    @api.expect(token_parser)
    @api.marshal_with(tokens, code=204, description='OK')
    @api.response(code=401, description='Invalid refresh token')
    @api.response(404, "Not Found")
    def put(self):
        """Проверка токенов на валидность"""
        return auth_service.approve_refresh_token(token_parser.parse_args()['refresh_token'])
