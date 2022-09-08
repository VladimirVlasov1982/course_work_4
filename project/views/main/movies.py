from flask_restx import Namespace, Resource
from project.container import movie_service
from project.setup.api.models import movie
from project.setup.api.parsers import movie_parser

api = Namespace('movies')


@api.route('/')
class MoviesView(Resource):
    @api.expect(movie_parser)
    @api.marshal_with(movie, as_list=True, code=200, description="OK")
    def get(self):
        """Получить все фильмы"""
        return movie_service.get_all_movie(**movie_parser.parse_args())


@api.route('/<int:movie_id>')
class MovieView(Resource):
    @api.response(400, "Not found")
    @api.marshal_with(movie, code=200, description="OK")
    def get(self, movie_id: int):
        """Получить фильм по id"""
        return movie_service.get_item(movie_id)
