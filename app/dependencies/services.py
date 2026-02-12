from dishka import Scope, provide, Provider
from redis.asyncio.client import Redis
from types_aiobotocore_s3 import S3Client

from cache import CountryCacheInvalidator, GenreCacheInvalidator, PersonCacheInvalidator, MoviePersonCacheInvalidator
from cache.invalidator import CacheInvalidatorBase
from cache.movie import MovieCacheInvalidator
from core.config import settings
from elastic.country import CountryElasticSyncer
from elastic.genre import GenreElasticSyncer
from elastic.movie import MovieElasticSyncer
from elastic.person import PersonElasticSyncer
from schemas.cache import ModelCacheConfig
from services.country import CountryService, CountrySearchService
from services.genre import GenreService, GenreSearchService
from services.m2m import MovieCountryService, MovieGenreService, MoviePersonService
from services.movie import MovieService, MovieFileService, MovieSearchService, MovieFilterService
from services.movie_shot import MovieShotService, MovieShotFileService
from services.person import PersonService, PersonFileService, PersonSearchService
from services.s3 import S3Service


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_s3_service(self, client: S3Client) -> S3Service:
        return S3Service(client=client, bucket_name=settings.s3.bucket_name)

    @provide
    def get_movie_cache_invalidator(self, cache: Redis) -> MovieCacheInvalidator:
        return MovieCacheInvalidator(cache)

    @provide
    def get_country_invalidator(self, cache: Redis) -> CountryCacheInvalidator:
        return CountryCacheInvalidator(
            CacheInvalidatorBase(cache, ModelCacheConfig(), "countries")
        )

    @provide
    def get_genre_invalidator(self, cache: Redis) -> GenreCacheInvalidator:
        return GenreCacheInvalidator(
            CacheInvalidatorBase(cache, ModelCacheConfig(), "genres")
        )

    @provide
    def get_person_invalidator(self, cache: Redis) -> PersonCacheInvalidator:
        return PersonCacheInvalidator(
            CacheInvalidatorBase(cache, ModelCacheConfig(), "persons")
        )

    @provide
    def get_movie_person_invalidator(self, cache: Redis) -> MoviePersonCacheInvalidator:
        return MoviePersonCacheInvalidator(
            CacheInvalidatorBase(cache, ModelCacheConfig(), "movie_person_associations")
        )

    get_country_syncer = provide(CountryElasticSyncer)
    get_genre_syncer = provide(GenreElasticSyncer)
    get_person_syncer = provide(PersonElasticSyncer)
    get_movie_syncer = provide(MovieElasticSyncer)

    get_movie_service = provide(MovieService)
    get_movie_file_service = provide(MovieFileService)
    get_movie_search_service = provide(MovieSearchService)
    get_movie_filter_service = provide(MovieFilterService)

    get_person_service = provide(PersonService)
    get_person_file_service = provide(PersonFileService)
    get_person_search_service = provide(PersonSearchService)

    get_genre_service = provide(GenreService)
    get_genre_search_service = provide(GenreSearchService)

    get_country_service = provide(CountryService)
    get_country_search_service = provide(CountrySearchService)

    get_movie_shot_service = provide(MovieShotService)
    get_movie_shot_file_service = provide(MovieShotFileService)

    get_movie_country_service = provide(MovieCountryService)
    get_movie_genre_service = provide(MovieGenreService)
    get_movie_person_service = provide(MoviePersonService)
