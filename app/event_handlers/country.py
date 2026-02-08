from pydantic import TypeAdapter

from cache import CountryCacheInvalidator
from core import fs_router
from elastic.country import CountryElasticSyncer
from schemas.base import Id
from schemas.country import CountryCreateEvent, CountryUpdateEvent, CountryElasticSchema
from dishka.integrations.faststream import FromDishka


@fs_router.subscriber("countries.created")
async def countries_created_invalidate_countries_list_cache(
        payload: CountryCreateEvent,
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("countries.bulk.created")
async def countries_bulk_created_invalidate_countries_list_cache(
        payload: list[CountryCreateEvent],
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("countries.updated")
async def countries_updated_invalidate_countries_list_cache(
        payload: CountryUpdateEvent,
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("countries.updated")
async def countries_updated_invalidate_countries_retrieve_cache(
        payload: CountryUpdateEvent,
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber("countries.deleted")
async def countries_deleted_invalidate_countries_list_cache(
        payload: Id,
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("countries.deleted")
async def countries_deleted_invalidate_countries_retrieve_cache(
        payload: Id,
        cache_invalidator: FromDishka[CountryCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber("countries.created")
async def countries_created_sync_elastic(
        payload: CountryCreateEvent,
        syncer: FromDishka[CountryElasticSyncer]
) -> None:
    await syncer.upsert(CountryElasticSchema.model_validate(payload))


@fs_router.subscriber("countries.bulk.created")
async def countries_bulk_created_sync_elastic(
        payload: list[CountryCreateEvent],
        syncer: FromDishka[CountryElasticSyncer]
) -> None:
    await syncer.bulk_upsert(TypeAdapter(list[CountryElasticSchema]).validate_python(payload))


@fs_router.subscriber("countries.updated")
async def countries_updated_sync_elastic(
        payload: CountryUpdateEvent,
        syncer: FromDishka[CountryElasticSyncer]
) -> None:
    await syncer.upsert(CountryElasticSchema.model_validate(payload))


@fs_router.subscriber("countries.deleted")
async def countries_deleted_sync_elastic(
        payload: Id,
        syncer: FromDishka[CountryElasticSyncer]
) -> None:
    await syncer.delete(payload.id)
