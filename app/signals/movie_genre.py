from core import fs_router
from schemas.base import Id
from schemas.event import BaseEventPublishers
from schemas.movie_genre import MovieGenreCreateEvent, MovieGenreUpdateEvent

movie_genre_created = fs_router.publisher(
    "movie.genre.associations.created",
    schema=MovieGenreCreateEvent,
)

movie_genre_bulk_created = fs_router.publisher(
    "movie.genre.associations.bulk.created",
    schema=list[MovieGenreCreateEvent],
)

movie_genre_updated = fs_router.publisher(
    "movie.genre.associations.updated",
    schema=MovieGenreUpdateEvent,
)

movie_genre_deleted = fs_router.publisher(
    "movie.genre.associations.deleted",
    schema=Id,
)

movie_genre_base_publishers = BaseEventPublishers(
    create_pub=movie_genre_created,
    bulk_create_pub=movie_genre_bulk_created,
    update_pub=movie_genre_updated,
    delete_pub=movie_genre_deleted,
)
