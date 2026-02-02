from core import fs_router
from schemas.base import Id
from schemas.genre import GenreCreateEvent, GenreUpdateEvent
from schemas.event import BaseEventPublishers

genre_created = fs_router.publisher(
    "genres.created",
    schema=GenreCreateEvent,
)

genre_bulk_created = fs_router.publisher(
    "genres.bulk.created",
    schema=list[GenreCreateEvent],
)

genre_updated = fs_router.publisher(
    "genres.updated",
    schema=GenreUpdateEvent,
)

genre_deleted = fs_router.publisher(
    "genres.deleted",
    schema=Id,
)

genre_base_publishers = BaseEventPublishers(
    create_pub=genre_created,
    bulk_create_pub=genre_bulk_created,
    update_pub=genre_updated,
    delete_pub=genre_deleted,
)