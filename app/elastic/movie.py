from elasticsearch import AsyncElasticsearch

from elastic.syncer import ElasticSyncer
from schemas.movie import MovieElasticSchema, MovieElasticUpdateSchema, MovieElasticBulkUpdateSchema


class MovieElasticSyncer(
    ElasticSyncer[
        MovieElasticSchema,
        MovieElasticUpdateSchema,
        MovieElasticBulkUpdateSchema
    ]
):
    def __init__(self, client: AsyncElasticsearch) -> None:
        super().__init__(client, "movies")
