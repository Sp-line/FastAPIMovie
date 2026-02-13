from faststream import AckPolicy
from nats.js.api import DeliverPolicy
from pydantic import TypeAdapter

from cache import PersonCacheInvalidator
from core import fs_router, stream
from elastic.person import PersonElasticSyncer
from schemas.base import Id
from schemas.person import PersonCreateEvent, PersonUpdateEvent, PersonElasticSchema
from dishka.integrations.faststream import FromDishka


@fs_router.subscriber(
    "catalog.persons.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def persons_created_invalidate_persons_list_cache(
        payload: PersonCreateEvent,
        cache_invalidator: FromDishka[PersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.persons.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def persons_bulk_created_invalidate_persons_list_cache(
        payload: list[PersonCreateEvent],
        cache_invalidator: FromDishka[PersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.persons.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def persons_updated_invalidate_persons_list_cache(
        payload: PersonUpdateEvent,
        cache_invalidator: FromDishka[PersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.persons.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def persons_updated_invalidate_persons_retrieve_cache(
        payload: PersonUpdateEvent,
        cache_invalidator: FromDishka[PersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber(
    "catalog.persons.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def persons_deleted_invalidate_persons_list_cache(
        payload: Id,
        cache_invalidator: FromDishka[PersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.persons.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def persons_deleted_invalidate_persons_retrieve_cache(
        payload: Id,
        cache_invalidator: FromDishka[PersonCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber(
    "catalog.persons.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def persons_created_sync_elastic(
        payload: PersonCreateEvent,
        syncer: FromDishka[PersonElasticSyncer]
) -> None:
    await syncer.upsert(PersonElasticSchema.model_validate(payload))


@fs_router.subscriber(
    "catalog.persons.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def persons_bulk_created_sync_elastic(
        payload: list[PersonCreateEvent],
        syncer: FromDishka[PersonElasticSyncer]
) -> None:
    await syncer.bulk_upsert(TypeAdapter(list[PersonElasticSchema]).validate_python(payload))


@fs_router.subscriber(
    "catalog.persons.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def persons_updated_sync_elastic(
        payload: PersonUpdateEvent,
        syncer: FromDishka[PersonElasticSyncer]
) -> None:
    await syncer.upsert(PersonElasticSchema.model_validate(payload))


@fs_router.subscriber(
    "catalog.persons.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def persons_deleted_sync_elastic(
        payload: Id,
        syncer: FromDishka[PersonElasticSyncer]
) -> None:
    await syncer.delete(payload.id)