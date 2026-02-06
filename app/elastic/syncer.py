from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from schemas.base import Id


class ElasticSyncer[
    TElasticSchema: Id,
]:
    def __init__(self, client: AsyncElasticsearch, index_name: str) -> None:
        self.client = client
        self._index_name = index_name

    async def upsert(self, data: TElasticSchema) -> None:
        await self.client.index(
            index=self._index_name,
            id=str(data.id),
            document=data.model_dump(),
            refresh=True
        )

    async def bulk_upsert(self, items: list[TElasticSchema]) -> None:
        if not items:
            return

        actions = [
            {
                "_op_type": "index",
                "_index": self._index_name,
                "_id": str(data.id),
                "_source": data.model_dump(),
            }
            for data in items
        ]

        await async_bulk(client=self.client, actions=actions, refresh=True)

    async def delete(self, document_id: int) -> None:
        await self.client.delete(
            index=self._index_name,
            id=str(document_id),
        )