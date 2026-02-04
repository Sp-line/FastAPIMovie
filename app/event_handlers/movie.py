from sqlalchemy import select

from core import fs_router
from core.models import MovieCountryAssociation, MovieGenreAssociation, MoviePersonAssociation
from dependencies.cache import MovieCacheInvalidatorDep
from dependencies.db import EventSessionDep
from schemas.base import Id
from schemas.country import CountryUpdateEvent
from schemas.genre import GenreUpdateEvent
from schemas.movie import MovieCreateEvent, MovieUpdateEvent
from schemas.movie_country import MovieCountryCreateEvent, MovieCountryDeleteEvent
from schemas.movie_genre import MovieGenreCreateEvent, MovieGenreDeleteEvent
from schemas.movie_person import MoviePersonCreateEvent, MoviePersonUpdateEvent, MoviePersonDeleteEvent
from schemas.movie_shot import MovieShotCreateEvent, MovieShotUpdateEvent, MovieShotDeleteEvent
from schemas.person import PersonUpdateEvent


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


@fs_router.subscriber("countries.updated")
async def countries_updated_invalidate_movies_detail_cache(
        payload: CountryUpdateEvent,
        session: EventSessionDep,
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    stmt = select(MovieCountryAssociation.movie_id).where(MovieCountryAssociation.country_id == payload.id)
    result = await session.execute(stmt)
    movie_ids = result.scalars().all()

    if movie_ids:
        await cache_invalidator.invalidate_detail_cache(*movie_ids)


@fs_router.subscriber("genres.updated")
async def genres_updated_invalidate_movies_detail_cache(
        payload: GenreUpdateEvent,
        session: EventSessionDep,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    stmt = select(MovieGenreAssociation.movie_id).where(MovieGenreAssociation.genre_id == payload.id)
    result = await session.execute(stmt)
    movie_ids = result.scalars().all()

    if movie_ids:
        await cache_invalidator.invalidate_detail_cache(*movie_ids)


@fs_router.subscriber("genres.updated")
async def genres_updated_invalidate_movies_list_summary_cache(
        payload: GenreUpdateEvent,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber("persons.updated")
async def persons_updated_invalidate_movies_detail_cache(
        payload: PersonUpdateEvent,
        session: EventSessionDep,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    stmt = select(MoviePersonAssociation.movie_id).where(MoviePersonAssociation.person_id == payload.id)
    result = await session.execute(stmt)
    movie_ids = result.scalars().all()

    if movie_ids:
        await cache_invalidator.invalidate_detail_cache(*movie_ids)


@fs_router.subscriber("movie.country.associations.created")
async def movie_country_created_invalidate_movies_detail_cache(
        payload: MovieCountryCreateEvent,
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber("movie.country.associations.bulk.created")
async def movie_country_bulk_created_invalidate_movies_detail_cache(
        payload: list[MovieCountryCreateEvent],
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    movie_ids = {event.movie_id for event in payload}

    await cache_invalidator.invalidate_detail_cache(*movie_ids)


@fs_router.subscriber("movie.genre.associations.created")
async def movie_genre_created_invalidate_movies_detail_cache(
        payload: MovieGenreCreateEvent,
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber("movie.genre.associations.bulk.created")
async def movie_genre_bulk_created_invalidate_movies_detail_cache(
        payload: list[MovieGenreCreateEvent],
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    movie_ids = {event.movie_id for event in payload}

    await cache_invalidator.invalidate_detail_cache(*movie_ids)


@fs_router.subscriber("movie.genre.associations.created")
async def movie_genre_created_invalidate_movies_list_summary_cache(
        payload: MovieGenreCreateEvent,
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber("movie.genre.associations.bulk.created")
async def movie_genre_bulk_created_invalidate_movies_list_summary_cache(
        payload: list[MovieGenreCreateEvent],
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber("movie.person.associations.created")
async def movie_person_created_invalidate_movies_detail_cache(
        payload: MoviePersonCreateEvent,
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber("movie.person.associations.created")
async def movie_person_bulk_created_invalidate_movies_detail_cache(
        payload: list[MoviePersonCreateEvent],
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    movie_ids = {event.movie_id for event in payload}

    await cache_invalidator.invalidate_detail_cache(*movie_ids)


@fs_router.subscriber("movie.person.associations.updated")
async def movie_person_updated_invalidate_movies_detail_cache(
        payload: MoviePersonUpdateEvent,
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber("movie.country.associations.deleted")
async def movie_country_deleted_invalidate_movies_detail_cache(
        payload: MovieCountryDeleteEvent,
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber("movie.genre.associations.deleted")
async def movie_genre_deleted_invalidate_movies_detail_cache(
        payload: MovieGenreDeleteEvent,
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber("movie.person.associations.deleted")
async def movie_person_deleted_invalidate_movies_detail_cache(
        payload: MoviePersonDeleteEvent,
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber("movie.genre.associations.deleted")
async def movie_genre_deleted_invalidate_movies_list_summary_cache(
        payload: MovieGenreDeleteEvent,
        cache_invalidator: MovieCacheInvalidatorDep,
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber("movies.created")
async def movies_created_invalidate_movies_list_summary_cache(
        payload: MovieCreateEvent,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber("movies.bulk.created")
async def movies_bulk_created_invalidate_movies_list_summary_cache(
        payload: list[MovieCreateEvent],
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber("movies.updated")
async def movies_updated_invalidate_movies_list_summary_cache(
        payload: MovieUpdateEvent,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber("movies.updated")
async def movies_updated_invalidate_movies_detail_cache(
        payload: MovieUpdateEvent,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.id)


@fs_router.subscriber("movies.deleted")
async def movies_deleted_invalidate_movies_list_summary_cache(
        payload: Id,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber("movies.deleted")
async def movies_deleted_invalidate_movies_detail_cache(
        payload: Id,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.id)


@fs_router.subscriber("movie.shot.created")
async def movie_shot_created_invalidate_movies_detail_cache(
        payload: MovieShotCreateEvent,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber("movie.shot.bulk.created")
async def movie_shot_bulk_created_invalidate_movies_detail_cache(
        payload: list[MovieShotCreateEvent],
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    movie_ids = {event.movie_id for event in payload}

    await cache_invalidator.invalidate_detail_cache(*movie_ids)


@fs_router.subscriber("movie.shot.updated")
async def movie_shot_updated_invalidate_movies_detail_cache(
        payload: MovieShotUpdateEvent,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber("movie.shot.deleted")
async def movie_shot_deleted_invalidate_movies_detail_cache(
        payload: MovieShotDeleteEvent,
        cache_invalidator: MovieCacheInvalidatorDep
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)
