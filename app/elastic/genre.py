from elasticsearch import AsyncElasticsearch

from elastic.syncer import ElasticSyncer
from schemas.genre import GenreElasticSchema, GenreElasticUpdateSchema, GenreElasticBulkUpdateSchema


class GenreElasticSyncer(
    ElasticSyncer[
        GenreElasticSchema,
        GenreElasticUpdateSchema,
        GenreElasticBulkUpdateSchema,
    ]
):
    def __init__(self, client: AsyncElasticsearch) -> None:
        super().__init__(client, "genres")