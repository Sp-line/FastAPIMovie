from core import fs_router
from dependencies.cache import GenreCacheInvalidatorDep
from schemas.base import Id
from schemas.genre import GenreCreateEvent, GenreUpdateEvent


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
