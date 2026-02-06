from pydantic import TypeAdapter

from core import fs_router
from dependencies.cache import GenreCacheInvalidatorDep
from dependencies.elastic import GenreElasticSyncerDep
from schemas.base import Id
from schemas.genre import GenreCreateEvent, GenreUpdateEvent, GenreElasticSchema


@fs_router.subscriber("genres.created")
async def genres_created_invalidate_genres_list_cache(
        payload: GenreCreateEvent,
        cache_invalidator: GenreCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("genres.bulk.created")
async def genres_bulk_created_invalidate_genres_list_cache(
        payload: list[GenreCreateEvent],
        cache_invalidator: GenreCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("genres.updated")
async def genres_updated_invalidate_genres_list_cache(
        payload: GenreUpdateEvent,
        cache_invalidator: GenreCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("genres.updated")
async def genres_updated_invalidate_genres_retrieve_cache(
        payload: GenreUpdateEvent,
        cache_invalidator: GenreCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber("genres.deleted")
async def genres_deleted_invalidate_genres_list_cache(
        payload: Id,
        cache_invalidator: GenreCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("genres.deleted")
async def genres_deleted_invalidate_genres_retrieve_cache(
        payload: Id,
        cache_invalidator: GenreCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber("genres.created")
async def genres_created_sync_elastic(
        payload: GenreCreateEvent,
        syncer: GenreElasticSyncerDep
) -> None:
    await syncer.upsert(GenreElasticSchema.model_validate(payload))


@fs_router.subscriber("genres.bulk.created")
async def genres_bulk_created_sync_elastic(
        payload: list[GenreCreateEvent],
        syncer: GenreElasticSyncerDep
) -> None:
    await syncer.bulk_upsert(TypeAdapter(list[GenreElasticSchema]).validate_python(payload))


@fs_router.subscriber("genres.updated")
async def genres_updated_sync_elastic(
        payload: GenreUpdateEvent,
        syncer: GenreElasticSyncerDep
) -> None:
    await syncer.upsert(GenreElasticSchema.model_validate(payload))


@fs_router.subscriber("genres.deleted")
async def genres_deleted_sync_elastic(
        payload: Id,
        syncer: GenreElasticSyncerDep
) -> None:
    await syncer.delete(payload.id)
