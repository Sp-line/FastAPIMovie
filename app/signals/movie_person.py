from core import fs_router
from schemas.base import Id
from schemas.event import BaseEventPublishers
from schemas.movie_person import MoviePersonCreateEvent, MoviePersonUpdateEvent

movie_person_created = fs_router.publisher(
    "movie.person.associations.created",
    schema=MoviePersonCreateEvent,
)

movie_person_bulk_created = fs_router.publisher(
    "movie.person.associations.bulk.created",
    schema=list[MoviePersonCreateEvent],
)

movie_person_updated = fs_router.publisher(
    "movie.person.associations.updated",
    schema=MoviePersonUpdateEvent,
)

movie_person_deleted = fs_router.publisher(
    "movie.person.associations.deleted",
    schema=Id,
)

movie_person_base_publishers = BaseEventPublishers(
    create_pub=movie_person_created,
    bulk_create_pub=movie_person_bulk_created,
    update_pub=movie_person_updated,
    delete_pub=movie_person_deleted,
)
