from typing import Annotated

from fastapi import Depends
from types_aiobotocore_s3.client import S3Client

from core.config import settings
from services.s3 import S3Service
from storage.s3 import s3_helper as s3


def get_s3_service(client: Annotated[S3Client, Depends(s3.get_client)]) -> S3Service:
    return S3Service(client=client, bucket_name=settings.s3.bucket_name)
