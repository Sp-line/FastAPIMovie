from elasticsearch import AsyncElasticsearch

from elastic.syncer import ElasticSyncer
from schemas.genre import GenreElasticSchema


class GenreElasticSyncer(ElasticSyncer[GenreElasticSchema]):
    def __init__(self, client: AsyncElasticsearch) -> None:
        super().__init__(client, "genres")