from core import fs_router
from dependencies.cache import MoviePersonCacheInvalidatorDep
from schemas.base import Id
from schemas.movie_person import MoviePersonCreateEvent, MoviePersonUpdateEvent


@fs_router.subscriber("movie.person.associations.created")
async def movie_person_created_invalidate_movie_person_associations_list_cache(
        payload: MoviePersonCreateEvent,
        cache_invalidator: MoviePersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("movie.person.associations.bulk.created")
async def movie_person_bulk_created_invalidate_movie_person_associations_list_cache(
        payload: list[MoviePersonCreateEvent],
        cache_invalidator: MoviePersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("movie.person.associations.updated")
async def movie_person_updated_invalidate_movie_person_associations_list_cache(
        payload: MoviePersonUpdateEvent,
        cache_invalidator: MoviePersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("movie.person.associations.updated")
async def movie_person_updated_invalidate_movie_person_associations_retrieve_cache(
        payload: MoviePersonUpdateEvent,
        cache_invalidator: MoviePersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber("movie.person.associations.deleted")
async def movie_person_deleted_invalidate_movie_person_associations_list_cache(
        payload: Id,
        cache_invalidator: MoviePersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber("movie.person.associations.deleted")
async def movie_person_deleted_invalidate_movie_person_associations_retrieve_cache(
        payload: Id,
        cache_invalidator: MoviePersonCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)
