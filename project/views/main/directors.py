from flask_restx import Resource, Namespace

from project.setup.api.models import director
from project.setup.api.parsers import page_parser
from project.container import director_service

api = Namespace('directors')


@api.route('/')
class DirectorsView(Resource):

    @api.expect(page_parser)
    @api.marshal_with(director, as_list=True, code=200, description="OK")
    def get(self):
        """Получить всех режиссеров"""
        return director_service.get_all(**page_parser.parse_args())


@api.route('/<int:director_id>')
class DirectorView(Resource):
    @api.response(404, "Not found")
    @api.marshal_with(director, code=200, description="OK")
    def get(self, director_id: int):
        """Получить одного режиссера"""
        return director_service.get_item(director_id)
