from fastapi import UploadFile
from pydantic import BaseModel

from exceptions.db import ObjectNotFoundException
from repositories.base import RepositoryBase
from repositories.unit_of_work import UnitOfWork
from services.s3 import S3Service
from storage.abc import FilePathBuilderABC, FileUrlResolverABC, FileServiceABC
from storage.transaction import FileTransaction
from tasks.s3 import delete_s3_file


class FileService[
    TReadSchema: BaseModel,
    TUpdateSchema: BaseModel
](FileServiceABC[TReadSchema]):
    def __init__(
            self,
            s3_service: S3Service,
            repository: RepositoryBase,
            unit_of_work: UnitOfWork,
            read_schema_type: type[TReadSchema],
            update_schema_type: type[TUpdateSchema],
            path_builder: FilePathBuilderABC[TReadSchema],
            url_resolver: FileUrlResolverABC,
            table_name: str,
            url_field: str,
    ) -> None:
        self._s3 = s3_service
        self._repository = repository
        self._uof = unit_of_work
        self._read_schema_type = read_schema_type
        self._update_schema_type = update_schema_type
        self._table_name = table_name
        self._path_builder = path_builder
        self._url_resolver = url_resolver
        self._url_field = url_field

    async def _get_obj(self, obj_id: int) -> TReadSchema:
        if not (obj := await self._repository.get_by_id(obj_id)):
            raise ObjectNotFoundException(obj_id, self._table_name)
        return self._read_schema_type.model_validate(obj)

    async def save(self, obj_id: int, file: UploadFile) -> TReadSchema:
        async with self._uof:
            obj = await self._get_obj(obj_id)
            old_url: str | None = getattr(obj, self._url_field, None)

            async with FileTransaction(self._s3, file, self._path_builder.build(obj)) as new_url:
                update_data = self._update_schema_type(
                    **{self._url_field: self._url_resolver.to_url(new_url)}
                )
                new_obj = self._read_schema_type.model_validate(await self._repository.update(obj_id, update_data))

        if old_url:
            await delete_s3_file.kiq(self._url_resolver.from_url(old_url))  # type: ignore[call-overload]

        return new_obj

    async def delete(self, obj_id: int) -> TReadSchema:
        async with self._uof:
            obj = await self._get_obj(obj_id)
            old_url = getattr(obj, self._url_field, None)

            update_data = self._update_schema_type(**{self._url_field: None})
            updated_obj = await self._repository.update(obj_id, update_data)

        if old_url:
            await delete_s3_file.kiq(self._url_resolver.from_url(old_url))  # type: ignore[call-overload]

        return self._read_schema_type.model_validate(updated_obj)
