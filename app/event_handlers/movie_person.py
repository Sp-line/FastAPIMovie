from faststream import AckPolicy
from nats.js.api import DeliverPolicy

from cache import MoviePersonCacheInvalidator
from core import fs_router, stream
from schemas.base import Id
from schemas.movie_person import MoviePersonCreateEvent, MoviePersonUpdateEvent
from dishka.integrations.faststream import FromDishka


@fs_router.subscriber(
    "catalog.movie.person.associations.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_created_invalidate_movie_person_associations_list_cache(
        payload: MoviePersonCreateEvent,
        cache_invalidator: FromDishka[MoviePersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.movie.person.associations.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_bulk_created_invalidate_movie_person_associations_list_cache(
        payload: list[MoviePersonCreateEvent],
        cache_invalidator: FromDishka[MoviePersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.movie.person.associations.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_updated_invalidate_movie_person_associations_list_cache(
        payload: MoviePersonUpdateEvent,
        cache_invalidator: FromDishka[MoviePersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.movie.person.associations.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_updated_invalidate_movie_person_associations_retrieve_cache(
        payload: MoviePersonUpdateEvent,
        cache_invalidator: FromDishka[MoviePersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber(
    "catalog.movie.person.associations.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_deleted_invalidate_movie_person_associations_list_cache(
        payload: Id,
        cache_invalidator: FromDishka[MoviePersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.movie.person.associations.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_deleted_invalidate_movie_person_associations_retrieve_cache(
        payload: Id,
        cache_invalidator: FromDishka[MoviePersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)
