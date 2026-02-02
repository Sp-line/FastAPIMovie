from core import fs_router
from dependencies.cache import MovieCacheInvalidatorDep
from schemas.base import Id
from schemas.movie import MovieCreateEvent, MovieUpdateEvent


@fs_router.subscriber("movies.created")
async def movies_created_invalidate_movies_list_cache(
        payload: MovieCreateEvent,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("movies.bulk.created")
async def movies_bulk_created_invalidate_movies_list_cache(
        payload: list[MovieCreateEvent],
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("movies.updated")
async def movies_updated_invalidate_movies_list_cache(
        payload: MovieUpdateEvent,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("movies.updated")
async def movies_updated_invalidate_movies_retrieve_cache(
        payload: MovieUpdateEvent,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber("movies.deleted")
async def movies_deleted_invalidate_movies_list_cache(
        payload: Id,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("movies.deleted")
async def movies_deleted_invalidate_movies_retrieve_cache(
        payload: Id,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)