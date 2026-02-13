from dishka.integrations.taskiq import FromDishka, inject

from core.taskiq_broker import broker
from elastic.country import CountryElasticSyncer
from elastic.genre import GenreElasticSyncer
from elastic.movie import MovieElasticSyncer
from elastic.person import PersonElasticSyncer
from schemas.country import CountryElasticSchema
from schemas.genre import GenreElasticSchema
from schemas.movie import MovieElasticSchema
from repositories.country import CountryRepository
from repositories.genre import GenreRepository
from repositories.movie import MovieRepository
from repositories.person import PersonRepository
from schemas.person import PersonElasticSchema
from utils.movie_elastic_adapter import MovieElasticAdapter


@broker.task(schedule=[{"cron": "0 3 */3 * *"}])
@inject(patch_module=True)
async def sync_countries_task(
        repository: FromDishka[CountryRepository],
        syncer: FromDishka[CountryElasticSyncer],
) -> None:
    items = [
        CountryElasticSchema.model_validate(country) for country in await repository.get_all()
    ]
    await syncer.bulk_upsert(items)


@broker.task(schedule=[{"cron": "0 3 */3 * *"}] )
@inject(patch_module=True)
async def sync_genres_task(
        repository: FromDishka[GenreRepository],
        syncer: FromDishka[GenreElasticSyncer],
) -> None:
    items = [
        GenreElasticSchema.model_validate(genre) for genre in await repository.get_all()
    ]
    await syncer.bulk_upsert(items)


@broker.task(schedule=[{"cron": "0 3 * * *"}])
@inject(patch_module=True)
async def sync_persons_task(
        repository: FromDishka[PersonRepository],
        syncer: FromDishka[PersonElasticSyncer],
) -> None:
    async for persons_batch in repository.get_for_elastic_sync_batched():
        items = [PersonElasticSchema.model_validate(person) for person in persons_batch]
        await syncer.bulk_upsert(items)


@broker.task(schedule=[{"cron": "0 3 * * *"}])
@inject(patch_module=True)
async def sync_movies_task(
        repository: FromDishka[MovieRepository],
        syncer: FromDishka[MovieElasticSyncer],
) -> None:
    async for movies_batch in repository.get_for_elastic_sync_batched():
        items = [
            MovieElasticSchema.model_validate(
                MovieElasticAdapter(
                    movie
                )
            ) for movie in movies_batch
        ]
        await syncer.bulk_upsert(items)
