from pydantic import TypeAdapter

from core import fs_router
from dependencies.cache import CountryCacheInvalidatorDep
from dependencies.elastic import AsyncElasticDep, CountryElasticSyncerDep
from schemas.base import Id
from schemas.country import CountryCreateEvent, CountryUpdateEvent, CountryElasticSchema


@fs_router.subscriber("countries.created")
async def countries_created_invalidate_countries_list_cache(
        payload: CountryCreateEvent,
        cache_invalidator: CountryCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("countries.bulk.created")
async def countries_bulk_created_invalidate_countries_list_cache(
        payload: list[CountryCreateEvent],
        cache_invalidator: CountryCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("countries.updated")
async def countries_updated_invalidate_countries_list_cache(
        payload: CountryUpdateEvent,
        cache_invalidator: CountryCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("countries.updated")
async def countries_updated_invalidate_countries_retrieve_cache(
        payload: CountryUpdateEvent,
        cache_invalidator: CountryCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber("countries.deleted")
async def countries_deleted_invalidate_countries_list_cache(
        payload: Id,
        cache_invalidator: CountryCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("countries.deleted")
async def countries_deleted_invalidate_countries_retrieve_cache(
        payload: Id,
        cache_invalidator: CountryCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber("countries.created")
async def countries_created_sync_elastic(
        payload: CountryCreateEvent,
        syncer: CountryElasticSyncerDep
) -> None:
    await syncer.upsert(CountryElasticSchema.model_validate(payload))


@fs_router.subscriber("countries.bulk.created")
async def countries_bulk_created_sync_elastic(
        payload: list[CountryCreateEvent],
        syncer: CountryElasticSyncerDep
) -> None:
    await syncer.bulk_upsert(TypeAdapter(list[CountryElasticSchema]).validate_python(payload))


@fs_router.subscriber("countries.updated")
async def countries_updated_sync_elastic(
        payload: CountryUpdateEvent,
        syncer: CountryElasticSyncerDep
) -> None:
    await syncer.upsert(CountryElasticSchema.model_validate(payload))


@fs_router.subscriber("countries.deleted")
async def countries_deleted_sync_elastic(
        payload: Id,
        syncer: CountryElasticSyncerDep
) -> None:
    await syncer.delete(payload.id)
