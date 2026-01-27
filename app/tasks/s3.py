from core import broker
from dependencies.s3 import S3ServiceTaskiqDep


@broker.task
async def delete_s3_file(obj_key: str, s3: S3ServiceTaskiqDep) -> None:
    await s3.delete_file(obj_key)
