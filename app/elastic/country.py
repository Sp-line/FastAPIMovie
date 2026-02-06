from elasticsearch import AsyncElasticsearch

from elastic.syncer import ElasticSyncer
from schemas.country import CountryElasticSchema


class CountryElasticSyncer(ElasticSyncer[CountryElasticSchema]):
    def __init__(self, client: AsyncElasticsearch) -> None:
        super().__init__(client, "countries")
