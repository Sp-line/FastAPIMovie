from core import fs_router
from schemas.base import Id
from schemas.movie import MovieCreateEvent, MovieUpdateEvent
from schemas.event import BaseEventPublishers

movie_created = fs_router.publisher(
    "movies.created",
    schema=MovieCreateEvent,
)

movie_bulk_created = fs_router.publisher(
    "movies.bulk.created",
    schema=list[MovieCreateEvent],
)

movie_updated = fs_router.publisher(
    "movies.updated",
    schema=MovieUpdateEvent,
)

movie_deleted = fs_router.publisher(
    "movies.deleted",
    schema=Id,
)

movie_base_publishers = BaseEventPublishers(
    create_pub=movie_created,
    bulk_create_pub=movie_bulk_created,
    update_pub=movie_updated,
    delete_pub=movie_deleted,
)