from elasticsearch import AsyncElasticsearch

from elastic.syncer import ElasticSyncer
from schemas.person import PersonElasticSchema


class PersonElasticSyncer(ElasticSyncer[PersonElasticSchema]):
    def __init__(self, client: AsyncElasticsearch) -> None:
        super().__init__(client, "persons")