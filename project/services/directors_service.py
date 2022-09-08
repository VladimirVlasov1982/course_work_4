from typing import Optional

from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import Director


class DirectorsService:
    def __init__(self, dao: BaseDAO):
        self.dao = dao

    def get_item(self, pk: int) -> Director:
        # Получение режиссера по id
        if director := self.dao.get_by_id(pk):
            return director
        raise ItemNotFound(f'Directors with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[Director]:
        # Получение всех режиссеров
        return self.dao.get_all(page=page)
