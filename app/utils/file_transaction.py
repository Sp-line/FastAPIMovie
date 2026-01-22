from fastapi import UploadFile

from services.s3 import S3Service


class FileTransaction:
    def __init__(self, files_service: S3Service, file: UploadFile | None, path: str) -> None:
        self._service = files_service
        self._file = file
        self._path = path
        self._uploaded_url: str | None = None

    async def __aenter__(self) -> str | None:
        if not self._file:
            return None

        self._uploaded_url = await self._service.upload_file(self._file, self._path)
        return self._uploaded_url

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: #todo types
        if exc_type and self._uploaded_url:
            await self._service.delete_file(self._uploaded_url) # todo send delete_file task
