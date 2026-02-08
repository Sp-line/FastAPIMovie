from dishka.integrations.taskiq import FromDishka, inject

from core import broker
from services.s3 import S3Service


@broker.task
@inject(patch_module=True)
async def delete_s3_file(obj_key: str, s3: FromDishka[S3Service]) -> None:
    await s3.delete_file(obj_key)
