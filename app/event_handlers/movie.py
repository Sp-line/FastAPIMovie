from faststream import AckPolicy
from nats.js.api import DeliverPolicy
from pydantic import TypeAdapter

from cache.movie import MovieCacheInvalidator
from core import fs_router, stream
from elastic.movie import MovieElasticSyncer
from repositories.m2m import MovieCountryRepository, MovieGenreRepository, MoviePersonRepository
from schemas.base import Id
from schemas.country import CountryUpdateEvent
from schemas.genre import GenreUpdateEvent
from schemas.movie import MovieCreateEvent, MovieUpdateEvent, MovieElasticSchema, MovieElasticUpdateSchema, \
    MovieElasticBulkUpdateSchema
from schemas.movie_country import MovieCountryCreateEvent, MovieCountryDeleteEvent
from schemas.movie_genre import MovieGenreCreateEvent, MovieGenreDeleteEvent
from schemas.movie_person import MoviePersonCreateEvent, MoviePersonUpdateEvent, MoviePersonDeleteEvent
from schemas.movie_shot import MovieShotCreateEvent, MovieShotUpdateEvent, MovieShotDeleteEvent
from schemas.person import PersonUpdateEvent
from dishka.integrations.faststream import FromDishka


@fs_router.subscriber(
    "catalog.movies.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_created_invalidate_movies_list_cache(
        payload: MovieCreateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.movies.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_bulk_created_invalidate_movies_list_cache(
        payload: list[MovieCreateEvent],
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.movies.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_updated_invalidate_movies_list_cache(
        payload: MovieUpdateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.movies.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_updated_invalidate_movies_retrieve_cache(
        payload: MovieUpdateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber(
    "catalog.movies.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_deleted_invalidate_movies_list_cache(
        payload: Id,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_cache()


@fs_router.subscriber(
    "catalog.movies.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_deleted_invalidate_movies_retrieve_cache(
        payload: Id,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_retrieve_cache(payload.id)


@fs_router.subscriber(
    "catalog.countries.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def countries_updated_invalidate_movies_detail_cache(
        payload: CountryUpdateEvent,
        movie_country_repo: FromDishka[MovieCountryRepository],
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    if movie_ids := await movie_country_repo.get_movie_ids_by_country_id(payload.id):
        await cache_invalidator.invalidate_detail_cache(*movie_ids)


@fs_router.subscriber(
    "catalog.genres.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_updated_invalidate_movies_detail_cache(
        payload: GenreUpdateEvent,
        movie_genre_repo: FromDishka[MovieGenreRepository],
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    if movie_ids := await movie_genre_repo.get_movie_ids_by_genre_id(payload.id):
        await cache_invalidator.invalidate_detail_cache(*movie_ids)


@fs_router.subscriber(
    "catalog.genres.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def genres_updated_invalidate_movies_list_summary_cache(
        payload: GenreUpdateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber(
    "catalog.persons.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def persons_updated_invalidate_movies_detail_cache(
        payload: PersonUpdateEvent,
        movie_person_repo: FromDishka[MoviePersonRepository],
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    if movie_ids := await movie_person_repo.get_movie_ids_by_person_id(payload.id):
        await cache_invalidator.invalidate_detail_cache(*movie_ids)


@fs_router.subscriber(
    "catalog.movie.country.associations.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_country_created_invalidate_movies_detail_cache(
        payload: MovieCountryCreateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber(
    "catalog.movie.country.associations.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_country_bulk_created_invalidate_movies_detail_cache(
        payload: list[MovieCountryCreateEvent],
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_detail_cache(
        *{event.movie_id for event in payload}
    )


@fs_router.subscriber(
    "catalog.movie.genre.associations.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_genre_created_invalidate_movies_detail_cache(
        payload: MovieGenreCreateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber(
    "catalog.movie.genre.associations.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_genre_bulk_created_invalidate_movies_detail_cache(
        payload: list[MovieGenreCreateEvent],
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_detail_cache(
        *{event.movie_id for event in payload}
    )


@fs_router.subscriber(
    "catalog.movie.genre.associations.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_genre_created_invalidate_movies_list_summary_cache(
        payload: MovieGenreCreateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber(
    "catalog.movie.genre.associations.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_genre_bulk_created_invalidate_movies_list_summary_cache(
        payload: list[MovieGenreCreateEvent],
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber(
    "catalog.movie.person.associations.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_created_invalidate_movies_detail_cache(
        payload: MoviePersonCreateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber(
    "catalog.movie.person.associations.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_bulk_created_invalidate_movies_detail_cache(
        payload: list[MoviePersonCreateEvent],
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_detail_cache(
        *{event.movie_id for event in payload}
    )


@fs_router.subscriber(
    "catalog.movie.person.associations.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_updated_invalidate_movies_detail_cache(
        payload: MoviePersonUpdateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber(
    "catalog.movie.country.associations.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_country_deleted_invalidate_movies_detail_cache(
        payload: MovieCountryDeleteEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber(
    "catalog.movie.genre.associations.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_genre_deleted_invalidate_movies_detail_cache(
        payload: MovieGenreDeleteEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber(
    "catalog.movie.person.associations.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_deleted_invalidate_movies_detail_cache(
        payload: MoviePersonDeleteEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber(
    "catalog.movie.genre.associations.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_genre_deleted_invalidate_movies_list_summary_cache(
        payload: MovieGenreDeleteEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator],
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber(
    "catalog.movies.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_created_invalidate_movies_list_summary_cache(
        payload: MovieCreateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber(
    "catalog.movies.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_bulk_created_invalidate_movies_list_summary_cache(
        payload: list[MovieCreateEvent],
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber(
    "catalog.movies.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_updated_invalidate_movies_list_summary_cache(
        payload: MovieUpdateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber(
    "catalog.movies.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_updated_invalidate_movies_detail_cache(
        payload: MovieUpdateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.id)


@fs_router.subscriber(
    "catalog.movies.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_deleted_invalidate_movies_list_summary_cache(
        payload: Id,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_list_summary_cache()


@fs_router.subscriber(
    "catalog.movies.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_deleted_invalidate_movies_detail_cache(
        payload: Id,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.id)


@fs_router.subscriber(
    "catalog.movie.shot.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_shot_created_invalidate_movies_detail_cache(
        payload: MovieShotCreateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber(
    "catalog.movie.shot.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_shot_bulk_created_invalidate_movies_detail_cache(
        payload: list[MovieShotCreateEvent],
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_detail_cache(
        *{event.movie_id for event in payload}
    )


@fs_router.subscriber(
    "catalog.movie.shot.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_shot_updated_invalidate_movies_detail_cache(
        payload: MovieShotUpdateEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber(
    "catalog.movie.shot.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_shot_deleted_invalidate_movies_detail_cache(
        payload: MovieShotDeleteEvent,
        cache_invalidator: FromDishka[MovieCacheInvalidator]
) -> None:
    await cache_invalidator.invalidate_detail_cache(payload.movie_id)


@fs_router.subscriber(
    "catalog.movies.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_bulk_created_sync_elastic(
        payload: list[MovieCreateEvent],
        syncer: FromDishka[MovieElasticSyncer]
) -> None:
    await syncer.bulk_upsert(TypeAdapter(list[MovieElasticSchema]).validate_python(payload))


@fs_router.subscriber(
    "catalog.movies.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_created_sync_elastic(
        payload: MovieCreateEvent,
        syncer: FromDishka[MovieElasticSyncer]
) -> None:
    await syncer.upsert(MovieElasticSchema.model_validate(payload))


@fs_router.subscriber(
    "catalog.movies.updated",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_updated_sync_elastic(
        payload: MovieUpdateEvent,
        syncer: FromDishka[MovieElasticSyncer]
) -> None:
    await syncer.update(payload.id, MovieElasticUpdateSchema.model_validate(payload))


@fs_router.subscriber(
    "catalog.movies.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movies_deleted_sync_elastic(
        payload: Id,
        syncer: FromDishka[MovieElasticSyncer]
) -> None:
    await syncer.delete(payload.id)


@fs_router.subscriber(
    "catalog.movie.genre.associations.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_genre_created_sync_elastic(
        payload: MovieGenreCreateEvent,
        syncer: FromDishka[MovieElasticSyncer],
        movie_genre_repo: FromDishka[MovieGenreRepository]
) -> None:
    genre_ids = await movie_genre_repo.get_genre_ids_by_movie_id(payload.movie_id)
    await syncer.update(payload.movie_id, MovieElasticUpdateSchema(genre_ids=list(genre_ids)))


@fs_router.subscriber(
    "catalog.movie.genre.associations.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_genre_bulk_created_sync_elastic(
        payload: list[MovieGenreCreateEvent],
        syncer: FromDishka[MovieElasticSyncer],
        movie_genre_repo: FromDishka[MovieGenreRepository]
) -> None:
    movie_ids_genre_ids_map = await movie_genre_repo.get_movie_ids_with_genre_ids_by_movie_ids(
        {event.movie_id for event in payload},
    )

    elastic_bulk_update_schemas = [
        MovieElasticBulkUpdateSchema(
            id=movie_id,
            genre_ids=genre_ids,
        )
        for movie_id, genre_ids in movie_ids_genre_ids_map.items()
    ]

    await syncer.bulk_update(elastic_bulk_update_schemas)


@fs_router.subscriber(
    "catalog.movie.genre.associations.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_genre_deleted_sync_elastic(
        payload: MovieGenreDeleteEvent,
        syncer: FromDishka[MovieElasticSyncer],
        movie_genre_repo: FromDishka[MovieGenreRepository]
) -> None:
    genre_ids = await movie_genre_repo.get_genre_ids_by_movie_id(payload.movie_id)
    await syncer.update(payload.movie_id, MovieElasticUpdateSchema(genre_ids=list(genre_ids)))


@fs_router.subscriber(
    "catalog.movie.country.associations.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_country_created_sync_elastic(
        payload: MovieCountryCreateEvent,
        syncer: FromDishka[MovieElasticSyncer],
        movie_country_repo: FromDishka[MovieCountryRepository]
) -> None:
    country_ids = await movie_country_repo.get_country_ids_by_movie_id(payload.movie_id)
    await syncer.update(payload.movie_id, MovieElasticUpdateSchema(country_ids=list(country_ids)))


@fs_router.subscriber(
    "catalog.movie.country.associations.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_country_bulk_created_sync_elastic(
        payload: list[MovieCountryCreateEvent],
        syncer: FromDishka[MovieElasticSyncer],
        movie_country_repo: FromDishka[MovieCountryRepository]
) -> None:
    movie_ids_country_ids_map = await movie_country_repo.get_movie_ids_with_country_ids_by_movie_ids(
        {event.movie_id for event in payload},
    )

    elastic_bulk_update_schemas = [
        MovieElasticBulkUpdateSchema(
            id=movie_id,
            country_ids=country_ids,
        )
        for movie_id, country_ids in movie_ids_country_ids_map.items()
    ]

    await syncer.bulk_update(elastic_bulk_update_schemas)


@fs_router.subscriber(
    "catalog.movie.country.associations.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_country_deleted_sync_elastic(
        payload: MovieCountryDeleteEvent,
        syncer: FromDishka[MovieElasticSyncer],
        movie_country_repo: FromDishka[MovieCountryRepository]
) -> None:
    country_ids = await movie_country_repo.get_country_ids_by_movie_id(payload.movie_id)
    await syncer.update(payload.movie_id, MovieElasticUpdateSchema(country_ids=list(country_ids)))


@fs_router.subscriber(
    "catalog.movie.person.associations.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_created_sync_elastic(
        payload: MoviePersonCreateEvent,
        syncer: FromDishka[MovieElasticSyncer],
        movie_person_repo: FromDishka[MoviePersonRepository]
) -> None:
    person_ids = await movie_person_repo.get_person_ids_by_movie_id(payload.movie_id)
    await syncer.update(payload.movie_id, MovieElasticUpdateSchema(person_ids=list(person_ids)))


@fs_router.subscriber(
    "catalog.movie.person.associations.bulk.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_bulk_created_sync_elastic(
        payload: list[MoviePersonCreateEvent],
        syncer: FromDishka[MovieElasticSyncer],
        movie_person_repo: FromDishka[MoviePersonRepository]
) -> None:
    movie_ids_person_ids_map = await movie_person_repo.get_movie_ids_with_person_ids_by_movie_ids(
        {event.movie_id for event in payload},
    )

    elastic_bulk_update_schemas = [
        MovieElasticBulkUpdateSchema(
            id=movie_id,
            person_ids=person_ids,
        )
        for movie_id, person_ids in movie_ids_person_ids_map.items()
    ]

    await syncer.bulk_update(elastic_bulk_update_schemas)


@fs_router.subscriber(
    "catalog.movie.person.associations.deleted",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def movie_person_deleted_sync_elastic(
        payload: MoviePersonDeleteEvent,
        syncer: FromDishka[MovieElasticSyncer],
        movie_person_repo: FromDishka[MoviePersonRepository]
) -> None:
    person_ids = await movie_person_repo.get_person_ids_by_movie_id(payload.movie_id)
    await syncer.update(payload.movie_id, MovieElasticUpdateSchema(person_ids=list(person_ids)))
