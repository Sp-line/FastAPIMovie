from typing import Any

from core.models import Movie


class MovieElasticAdapter:
    def __init__(self, movie: Movie):
        self._movie = movie

    @property
    def genre_ids(self) -> list[int]:
        return [assoc.genre_id for assoc in self._movie.genre_associations]

    @property
    def country_ids(self) -> list[int]:
        return [assoc.country_id for assoc in self._movie.country_associations]

    @property
    def person_ids(self) -> list[int]:
        return [assoc.person_id for assoc in self._movie.person_associations]

    def __getattr__(self, item: str) -> Any:
        return getattr(self._movie, item)