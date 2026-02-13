from dishka.integrations.faststream import FromDishka
from faststream import AckPolicy
from nats.js.api import DeliverPolicy
from pydantic import TypeAdapter

from cache import CountryCacheInvalidator
from core import fs_router, stream
from elastic.country import CountryElasticSyncer
from schemas.base import Id
from schemas.country import CountryCreateEvent, CountryUpdateEvent, CountryElasticSchema, CountryElasticUpdateSchema


@fs_router.subscriber(
    "catalog.countries.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def countries_created_invalidate_countries_list_cache(
        payload: CountryCreateEvent,
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.countries.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def countries_bulk_created_invalidate_countries_list_cache(
        payload: list[CountryCreateEvent],
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.countries.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def countries_updated_invalidate_countries_list_cache(
        payload: CountryUpdateEvent,
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.countries.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def countries_updated_invalidate_countries_retrieve_cache(
        payload: CountryUpdateEvent,
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber(
    "catalog.countries.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def countries_deleted_invalidate_countries_list_cache(
        payload: Id,
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.countries.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def countries_deleted_invalidate_countries_retrieve_cache(
        payload: Id,
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber(
    "catalog.countries.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def countries_created_sync_elastic(
        payload: CountryCreateEvent,
        syncer: FromDishka[CountryElasticSyncer]
) -> None:
    await syncer.upsert(CountryElasticSchema.model_validate(payload))


@fs_router.subscriber(
    "catalog.countries.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def countries_bulk_created_sync_elastic(
        payload: list[CountryCreateEvent],
        syncer: FromDishka[CountryElasticSyncer]
) -> None:
    await syncer.bulk_upsert(TypeAdapter(list[CountryElasticSchema]).validate_python(payload))


@fs_router.subscriber(
    "catalog.countries.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def countries_updated_sync_elastic(
        payload: CountryUpdateEvent,
        syncer: FromDishka[CountryElasticSyncer]
) -> None:
    await syncer.update(payload.id, CountryElasticUpdateSchema.model_validate(payload))


@fs_router.subscriber(
    "catalog.countries.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def countries_deleted_sync_elastic(
        payload: Id,
        syncer: FromDishka[CountryElasticSyncer]
) -> None:
    await syncer.delete(payload.id)
