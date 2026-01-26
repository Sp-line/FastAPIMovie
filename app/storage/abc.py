from abc import ABC, abstractmethod

from fastapi import UploadFile
from pydantic import BaseModel


class FileServiceABC[TReadSchema: BaseModel](ABC):
    @abstractmethod
    async def save(self, obj_id: int, file: UploadFile) -> TReadSchema: ...

    @abstractmethod
    async def delete(self, obj_id: int) -> TReadSchema: ...


class FilePathBuilderABC[TReadSchema: BaseModel](ABC):
    @abstractmethod
    def build(self, obj: TReadSchema) -> str: ...


class FileUrlResolverABC(ABC):
    @abstractmethod
    def to_url(self, path: str) -> str: ...

    @abstractmethod
    def from_url(self, url: str) -> str: ...