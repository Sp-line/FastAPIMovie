from elasticsearch import AsyncElasticsearch

from elastic.syncer import ElasticSyncer
from schemas.person import PersonElasticSchema, PersonElasticUpdateSchema, PersonElasticBulkUpdateSchema


class PersonElasticSyncer(
    ElasticSyncer[
        PersonElasticSchema,
        PersonElasticUpdateSchema,
        PersonElasticBulkUpdateSchema,
    ]
):
    def __init__(self, client: AsyncElasticsearch) -> None:
        super().__init__(client, "persons")