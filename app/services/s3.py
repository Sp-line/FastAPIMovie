from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from botocore.exceptions import ClientError
from fastapi import UploadFile

from exceptions.s3 import S3UploadException, S3DeleteException

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client


class S3Service:
    def __init__(self, client: S3Client, bucket_name: str):
        self.client = client
        self.bucket_name = bucket_name

    @staticmethod
    def generate_file_name(name: str | None, file: UploadFile) -> str:
        s3_key_base = name or file.filename or "file"

        parts = file.filename.rsplit(".", 1)
        extension = parts[1] if len(parts) == 2 else ""
        unique_id = uuid.uuid4().hex[:8]

        file_name = f"{s3_key_base}-{unique_id}"
        if extension:
            return f"{file_name}.{extension}"
        return file_name

    async def upload_file(
            self,
            file: UploadFile,
            obj_name: str | None = None
    ) -> str:
        s3_key = self.generate_file_name(obj_name, file)

        try:
            await file.seek(0)
            await self.client.upload_fileobj(
                Fileobj=file.file,
                Bucket=self.bucket_name,
                Key=s3_key,
                ExtraArgs={'ContentType': file.content_type}
            )
            return s3_key

        except ClientError as e:
            raise S3UploadException(s3_key) from e

    async def delete_file(self, obj_name: str) -> None:
        try:
            await self.client.delete_object(Bucket=self.bucket_name, Key=obj_name)
        except ClientError as e:
            raise S3DeleteException(obj_name) from e
