from core import fs_router
from schemas.base import Id
from schemas.event import BaseEventPublishers
from schemas.movie_shot import MovieShotCreateEvent, MovieShotUpdateEvent

movie_shot_created = fs_router.publisher(
    "catalog.movie.shot.created",
    schema=MovieShotCreateEvent,
)

movie_shot_bulk_created = fs_router.publisher(
    "catalog.movie.shot.bulk.created",
    schema=list[MovieShotCreateEvent],
)

movie_shot_updated = fs_router.publisher(
    "catalog.movie.shot.updated",
    schema=MovieShotUpdateEvent,
)

movie_shot_deleted = fs_router.publisher(
    "catalog.movie.shot.deleted",
    schema=Id,
)

movie_shot_base_publishers = BaseEventPublishers(
    create_pub=movie_shot_created,
    bulk_create_pub=movie_shot_bulk_created,
    update_pub=movie_shot_updated,
    delete_pub=movie_shot_deleted,
)
