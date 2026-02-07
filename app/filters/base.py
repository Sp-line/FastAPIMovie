from abc import ABC, abstractmethod
from typing import Any

from elasticsearch.dsl import AsyncSearch, Q

from filters.types import RangeOperator


class FilterStrategy(ABC):
    @abstractmethod
    def apply(self, search: AsyncSearch, value: Any) -> AsyncSearch:
        pass


class RangeFilter(FilterStrategy):
    def __init__(self, field: str, operator: RangeOperator):
        self._field = field
        self._operator = operator

    def apply(self, search: AsyncSearch, value: Any) -> AsyncSearch:
        return search.filter("range", **{self._field: {self._operator: value}})


class TermFilter(FilterStrategy):
    def __init__(self, field: str):
        self._field = field

    def apply(self, search: AsyncSearch, value: Any) -> AsyncSearch:
        if isinstance(value, list):
            return search.filter("terms", **{self._field: value})
        return search.filter("term", **{self._field: value})


class WeightedTermFilter(FilterStrategy):
    def __init__(self, field: str):
        self.field = field

    def apply(self, search: AsyncSearch, value: Any) -> AsyncSearch:
        if isinstance(value, list):
            return search.query("bool", should=[
                Q("term", **{self.field: item}) for item in value
            ])
        return search.query("term", **{self.field: value})
