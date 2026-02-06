from pydantic import TypeAdapter

from core import fs_router
from dependencies.cache import PersonCacheInvalidatorDep
from dependencies.elastic import PersonElasticSyncerDep
from schemas.base import Id
from schemas.person import PersonCreateEvent, PersonUpdateEvent, PersonElasticSchema


@fs_router.subscriber("persons.created")
async def persons_created_invalidate_persons_list_cache(
        payload: PersonCreateEvent,
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("persons.bulk.created")
async def persons_bulk_created_invalidate_persons_list_cache(
        payload: list[PersonCreateEvent],
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("persons.updated")
async def persons_updated_invalidate_persons_list_cache(
        payload: PersonUpdateEvent,
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("persons.updated")
async def persons_updated_invalidate_persons_retrieve_cache(
        payload: PersonUpdateEvent,
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber("persons.deleted")
async def persons_deleted_invalidate_persons_list_cache(
        payload: Id,
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("persons.deleted")
async def persons_deleted_invalidate_persons_retrieve_cache(
        payload: Id,
        cache_invalidator: PersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber("persons.created")
async def persons_created_sync_elastic(
        payload: PersonCreateEvent,
        syncer: PersonElasticSyncerDep
) -> None:
    await syncer.upsert(PersonElasticSchema.model_validate(payload))


@fs_router.subscriber("persons.bulk.created")
async def persons_bulk_created_sync_elastic(
        payload: list[PersonCreateEvent],
        syncer: PersonElasticSyncerDep
) -> None:
    await syncer.bulk_upsert(TypeAdapter(list[PersonElasticSchema]).validate_python(payload))


@fs_router.subscriber("persons.updated")
async def persons_updated_sync_elastic(
        payload: PersonUpdateEvent,
        syncer: PersonElasticSyncerDep
) -> None:
    await syncer.upsert(PersonElasticSchema.model_validate(payload))


@fs_router.subscriber("persons.deleted")
async def persons_deleted_sync_elastic(
        payload: Id,
        syncer: PersonElasticSyncerDep
) -> None:
    await syncer.delete(payload.id)