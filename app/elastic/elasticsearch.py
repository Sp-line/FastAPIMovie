from elasticsearch import AsyncElasticsearch

from core.config import settings
from elastic import documents_init
from exceptions.elastic import ElasticClientNotInitializedException, ElasticConnectionFailed


class ElasticsearchHelper:
    def __init__(self, url: str) -> None:
        self._client: AsyncElasticsearch | None = None
        self._url = url

    async def connect(self) -> None:
        self._client = AsyncElasticsearch(self._url)
        if not await self._client.ping():
            raise ElasticConnectionFailed()

    async def documents_init(self):
        await documents_init(self.get_client())

    async def close(self) -> None:
        if self._client:
            await self._client.close()
            self._client = None

    def get_client(self) -> AsyncElasticsearch:
        if self._client is None:
            raise ElasticClientNotInitializedException()
        return self._client


es_helper = ElasticsearchHelper(str(settings.elasticsearch.url))
