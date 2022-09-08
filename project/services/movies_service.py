from typing import Optional

from project.dao import MoviesDAO
from project.exceptions import ItemNotFound
from project.models import Movie


class MoviesService:
    def __init__(self, dao: MoviesDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> Movie:
        # Получение фильма по id
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f"Movie with pk={pk} not found")

    def get_all_movie(self, status: str, page: Optional[int] = None) -> list[Movie]:
        # Получение всех фильмов
        return self.dao.get_all_movie(page=page, status=status)
