from typing import Optional

from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import Movie


class MoviesService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_all(self, status: str, page: Optional[int] = None) -> list[Movie]:
        return self.dao.get_all(page=page, status=status)

    def get_item(self, pk: int) -> Movie:
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f"Movie {pk} not found")
