from core import fs_router
from schemas.base import Id
from schemas.event import BaseEventPublishers
from schemas.movie_country import MovieCountryCreateEvent, MovieCountryUpdateEvent

movie_country_created = fs_router.publisher(
    "movie.country.associations.created",
    schema=MovieCountryCreateEvent,
)

movie_country_bulk_created = fs_router.publisher(
    "movie.country.associations.bulk.created",
    schema=list[MovieCountryCreateEvent],
)

movie_country_updated = fs_router.publisher(
    "movie.country.associations.updated",
    schema=MovieCountryUpdateEvent,
)

movie_country_deleted = fs_router.publisher(
    "movie.country.associations.deleted",
    schema=Id,
)

movie_country_base_publishers = BaseEventPublishers(
    create_pub=movie_country_created,
    bulk_create_pub=movie_country_bulk_created,
    update_pub=movie_country_updated,
    delete_pub=movie_country_deleted,
)
