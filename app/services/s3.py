from __future__ import annotations

import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from botocore.exceptions import ClientError
from fastapi import UploadFile
from slugify import slugify

from exceptions.s3 import S3UploadException, S3DeleteException

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client


class S3Service:
    def __init__(self, client: S3Client, bucket_name: str):
        self.client = client
        self.bucket_name = bucket_name

    @staticmethod
    def generate_file_name(file: UploadFile, name: str | None = None) -> str:
        uploaded_path = Path(file.filename or "file")
        suffix = uploaded_path.suffix.lower()

        if name:
            base_name = name
        else:
            base_name = uploaded_path.stem

        safe_name = slugify(base_name)
        unique_id = uuid.uuid4().hex[:8]

        return f"{safe_name}_{unique_id}{suffix}"


    async def upload_file(
            self,
            file: UploadFile,
            obj_name: str | None = None
    ) -> str:
        s3_key = self.generate_file_name(file, obj_name)

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
