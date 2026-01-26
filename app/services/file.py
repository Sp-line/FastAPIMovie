from typing import Type

from fastapi import UploadFile
from pydantic import BaseModel
from slugify import slugify

from core.config import settings
from exceptions.db import ObjectNotFoundException
from repositories.base import IntRepositoryBase
from repositories.unit_of_work import UnitOfWork
from services.s3 import S3Service
from utils.file_transaction import FileTransaction


class FileService[ReadSchemaType]:
    def __init__(
            self,
            file_service: S3Service,
            repository: IntRepositoryBase,
            unit_of_work: UnitOfWork,
            read_schema_type: Type[BaseModel],
            update_schema_type: Type[BaseModel],
            table_name: str,
            folder: str,
            url_field: str,
            filename_field: str
    ) -> None:
        self._files = file_service
        self._repository = repository
        self._uof = unit_of_work
        self._read_schema_type = read_schema_type
        self._update_schema_type = update_schema_type
        self._table_name = table_name
        self._folder = folder
        self._url_field = url_field
        self._filename_field = filename_field

    async def update_file(self, obj_id: int, file: UploadFile) -> ReadSchemaType:
        obj = await self._repository.get_by_id(obj_id)
        if not obj:
            raise ObjectNotFoundException[int](obj_id, self._table_name)

        old_url: str | None = getattr(obj, self._url_field, None)
        s3_path = f"{self._folder}/{slugify(str(getattr(obj, self._filename_field)))}"
        base_url = f"{settings.s3.endpoint_url}{settings.s3.bucket_name}"

        async with FileTransaction(self._files, file, s3_path) as new_url:
            update_data = self._update_schema_type(
                **{self._url_field: f"{base_url}/{new_url}"}
            )

            async with self._uof:
                new_obj = self._read_schema_type.model_validate(await self._repository.update(obj_id, update_data))

        if old_url:
            await self._files.delete_file(old_url.removeprefix(base_url))

        return new_obj
