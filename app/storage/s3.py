import aioboto3

from core.config import settings
from exceptions.s3 import S3ClientNotInitializedException


class S3Helper:
    def __init__(
            self,
            endpoint_url: str,
            access_key: str,
            secret_key: str,
            region: str = "us-east-1",
    ) -> None:
        self.config = {
            "endpoint_url": endpoint_url,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "region_name": region,
        }
        self.session = aioboto3.Session()

        self._client = None
        self._exit_stack = None

    async def connect(self):
        self._exit_stack = await self.session.client("s3", **self.config).__aenter__()
        self._client = self._exit_stack

    async def close(self):
        if self._exit_stack:
            await self._exit_stack.__aexit__(None, None, None)

    def get_client(self):
        if self._client is None:
            raise S3ClientNotInitializedException()
        return self._client


s3_helper = S3Helper(
    endpoint_url=str(settings.s3.endpoint_url),
    access_key=settings.s3.access_key,
    secret_key=settings.s3.secret_key,
    region=settings.s3.region,
)
