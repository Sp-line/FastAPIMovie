from core import fs_router
from dependencies.cache import PersonCacheInvalidatorDep
from schemas.base import Id
from schemas.person import PersonCreateEvent, PersonUpdateEvent


@fs_router.subscriber("persons.created")
async def persons_created_invalidate_countries_list_cache(
        payload: PersonCreateEvent,
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("persons.bulk.created")
async def persons_bulk_created_invalidate_countries_list_cache(
        payload: list[PersonCreateEvent],
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("persons.updated")
async def persons_updated_invalidate_countries_list_cache(
        payload: PersonUpdateEvent,
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("persons.updated")
async def persons_updated_invalidate_countries_retrieve_cache(
        payload: PersonUpdateEvent,
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber("persons.deleted")
async def persons_deleted_invalidate_countries_list_cache(
        payload: Id,
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("persons.deleted")
async def persons_deleted_invalidate_countries_retrieve_cache(
        payload: Id,
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)
