from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser

auth_parser: RequestParser = RequestParser()
auth_parser.add_argument(name='email', type=email(), required=True, nullable=False)
auth_parser.add_argument(name='password', type=str, required=True, nullable=False)

change_password_parser: RequestParser = RequestParser()
change_password_parser.add_argument(name='old_password', type=str, required=True, nullable=False)
change_password_parser.add_argument(name='new_password', type=str, required=True, nullable=False)

change_user_info_parser: RequestParser = RequestParser()
change_user_info_parser.add_argument(name='name', type=str, required=True)
change_user_info_parser.add_argument(name='surname', type=str, required=True)
change_user_info_parser.add_argument(name='favourite_genre', type=int, required=True)

token_parser: RequestParser = RequestParser()
token_parser.add_argument(name='access_token', type=str, required=True)
token_parser.add_argument(name='refresh_token', type=str, required=True)

page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, location='args', required=False)

movie_parser: RequestParser = RequestParser()
movie_parser.add_argument(name='page', type=int, location='args', required=False)
movie_parser.add_argument(name='status', type=str, location='args', required=False)
