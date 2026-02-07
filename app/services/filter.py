from elasticsearch import AsyncElasticsearch
from elasticsearch.dsl import AsyncSearch
from pydantic import BaseModel

from filters.base import FilterStrategy
from schemas.base import Pagination


class FilterService[
    TFilterRegistry: BaseModel,
    TFilterSchema: Pagination,
    TReadSchema: BaseModel
]:
    def __init__(
            self,
            client: AsyncElasticsearch,
            filter_registry: TFilterRegistry,
            read_schema: type[TReadSchema],
            index: str
    ) -> None:
        self._client = client
        self._registry = filter_registry
        self._read_schema = read_schema
        self._index = index

    async def get(self, filters: TFilterSchema) -> list[TReadSchema]:
        s = AsyncSearch(using=self._client, index=self._index)
        filter_data = filters.model_dump(exclude_none=True)

        for field_name, value in filter_data.items():
            strategy = getattr(self._registry, field_name, None)
            if strategy and isinstance(strategy, FilterStrategy):
                s = strategy.apply(s, value)

        s = s[filters.skip: filters.skip + filters.limit]
        result = await s.execute()
        return [
            self._read_schema.model_validate(hit.to_dict())
            for hit in result.hits
        ]