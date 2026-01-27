from typing import Annotated, TypeAlias

from fastapi import Depends
from taskiq import TaskiqDepends
from types_aiobotocore_s3.client import S3Client

from core.config import settings
from services.s3 import S3Service
from storage.s3 import s3_helper as s3

S3ClientDep: TypeAlias = Annotated[S3Client, Depends(s3.get_client)]
S3ClientTaskiqDep: TypeAlias = Annotated[S3Client, TaskiqDepends(s3.get_client)]


def get_s3_service(client: S3ClientDep) -> S3Service:
    return S3Service(client=client, bucket_name=settings.s3.bucket_name)


def taskiq_get_s3_service(client: S3ClientTaskiqDep) -> S3Service:
    return S3Service(client=client, bucket_name=settings.s3.bucket_name)


S3ServiceDep: TypeAlias = Annotated[S3Service, Depends(get_s3_service)]
S3ServiceTaskiqDep: TypeAlias = Annotated[S3Service, TaskiqDepends(taskiq_get_s3_service)]
