from faststream import AckPolicy
from nats.js.api import DeliverPolicy
from pydantic import TypeAdapter

from cache import GenreCacheInvalidator
from core import fs_router, stream
from elastic.genre import GenreElasticSyncer
from schemas.base import Id
from schemas.genre import GenreCreateEvent, GenreUpdateEvent, GenreElasticSchema, GenreElasticUpdateSchema
from dishka.integrations.faststream import FromDishka


@fs_router.subscriber(
    "catalog.genres.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_created_invalidate_genres_list_cache(
        payload: GenreCreateEvent,
        cache_invalidator: FromDishka[GenreCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.genres.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_bulk_created_invalidate_genres_list_cache(
        payload: list[GenreCreateEvent],
        cache_invalidator: FromDishka[GenreCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.genres.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_updated_invalidate_genres_list_cache(
        payload: GenreUpdateEvent,
        cache_invalidator: FromDishka[GenreCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.genres.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_updated_invalidate_genres_retrieve_cache(
        payload: GenreUpdateEvent,
        cache_invalidator: FromDishka[GenreCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber(
    "catalog.genres.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_deleted_invalidate_genres_list_cache(
        payload: Id,
        cache_invalidator: FromDishka[GenreCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.genres.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_deleted_invalidate_genres_retrieve_cache(
        payload: Id,
        cache_invalidator: FromDishka[GenreCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber(
    "catalog.genres.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_created_sync_elastic(
        payload: GenreCreateEvent,
        syncer: FromDishka[GenreElasticSyncer]
) -> None:
    await syncer.upsert(GenreElasticSchema.model_validate(payload))


@fs_router.subscriber(
    "catalog.genres.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_bulk_created_sync_elastic(
        payload: list[GenreCreateEvent],
        syncer: FromDishka[GenreElasticSyncer]
) -> None:
    await syncer.bulk_upsert(TypeAdapter(list[GenreElasticSchema]).validate_python(payload))


@fs_router.subscriber(
    "catalog.genres.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_updated_sync_elastic(
        payload: GenreUpdateEvent,
        syncer: FromDishka[GenreElasticSyncer]
) -> None:
    await syncer.update(payload.id, GenreElasticUpdateSchema.model_validate(payload))


@fs_router.subscriber(
    "catalog.genres.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_deleted_sync_elastic(
        payload: Id,
        syncer: FromDishka[GenreElasticSyncer]
) -> None:
    await syncer.delete(payload.id)
