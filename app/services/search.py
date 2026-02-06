from elasticsearch import AsyncElasticsearch
from elasticsearch.dsl import AsyncSearch
from elasticsearch.dsl.query import MultiMatch
from pydantic import BaseModel


class SearchServiceBase[
    TSearchReadSchema: BaseModel,
]:
    def __init__(
            self,
            client: AsyncElasticsearch,
            read_schema: type[TSearchReadSchema],
            index: str,
            search_fields: list[str],
    ) -> None:
        self._client = client
        self._read_schema = read_schema
        self._index = index
        self._search_fields = search_fields

    async def search(self, query: str, skip: int = 0, limit: int = 10) -> list[TSearchReadSchema]:
        stmt = AsyncSearch(using=self._client, index=self._index).query(
            MultiMatch(
                query=query,
                fields=self._search_fields,
                fuzziness="AUTO"
            )
        )
        stmt = stmt[skip: skip + limit]
        result = await stmt.execute()
        return [
            self._read_schema.model_validate(hit.to_dict())
            for hit in result.hits
        ]
