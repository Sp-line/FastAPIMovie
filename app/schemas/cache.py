from abc import ABC, abstractmethod

from pydantic import BaseModel


class ModelCacheConfig(BaseModel, ABC):
    list_key: str = "{table_name}:list:skip={skip}:limit={limit}"
    list_ttl: int = 86400
    retrieve_key: str = "{table_name}:retrieve:id={obj_id}"
    retrieve_ttl: int = 86400
