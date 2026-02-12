from elasticsearch import AsyncElasticsearch

from elastic.syncer import ElasticSyncer
from schemas.country import CountryElasticSchema, CountryElasticUpdateSchema, CountryElasticBulkUpdateSchema


class CountryElasticSyncer(
    ElasticSyncer[
        CountryElasticSchema,
        CountryElasticUpdateSchema,
        CountryElasticBulkUpdateSchema
    ]
):
    def __init__(self, client: AsyncElasticsearch) -> None:
        super().__init__(client, "countries")
