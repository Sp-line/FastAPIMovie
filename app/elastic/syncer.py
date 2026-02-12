from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from pydantic import BaseModel

from schemas.base import Id


class ElasticSyncer[
    TElasticSchema: Id,
    TElasticUpdateSchema: BaseModel,
    TElasticBulkUpdateSchema: Id,
]:
    def __init__(self, client: AsyncElasticsearch, index_name: str) -> None:
        self.client = client
        self._index_name = index_name

    async def upsert(self, data: TElasticSchema) -> None:
        await self.client.index(
            index=self._index_name,
            id=str(data.id),
            document=data.model_dump(),
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

        await async_bulk(client=self.client, actions=actions)

    async def update(self, document_id: int, data: TElasticUpdateSchema) -> None:
        await self.client.update(
            index=self._index_name,
            id=str(document_id),
            doc=data.model_dump(exclude_unset=True),
            retry_on_conflict=3,
        )

    async def bulk_update(self, data: list[TElasticBulkUpdateSchema]) -> None:
        actions = [
            {
                "_op_type": "update",
                "_index": self._index_name,
                "_id": str(item.id),
                "retry_on_conflict": 3,
                "doc": item.model_dump(exclude_unset=True),
            }
            for item in data
        ]
        await async_bulk(client=self.client, actions=actions)

    async def delete(self, document_id: int) -> None:
        await self.client.delete(
            index=self._index_name,
            id=str(document_id),
        )