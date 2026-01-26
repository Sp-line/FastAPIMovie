from types import TracebackType

from fastapi import UploadFile

from exceptions.s3 import S3DeleteException
from services.s3 import S3Service


class FileTransaction:
    def __init__(self, files_service: S3Service, file: UploadFile, path: str) -> None:
        self._service = files_service
        self._file = file
        self._path = path
        self._uploaded_key: str | None = None

    async def __aenter__(self) -> str:
        self._uploaded_key = await self._service.upload_file(self._file, self._path)
        return self._uploaded_key

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> None:
        if exc_type and self._uploaded_key:
            try:
                await self._service.delete_file(self._uploaded_key)
            except S3DeleteException:
                pass
