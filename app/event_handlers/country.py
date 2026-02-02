from core import fs_router
from dependencies.cache import CountryCacheInvalidatorDep
from schemas.base import Id
from schemas.country import CountryCreateEvent, CountryUpdateEvent


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
