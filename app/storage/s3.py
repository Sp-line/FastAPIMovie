import aioboto3
from types_aiobotocore_s3 import S3Client

from core.config import settings
from exceptions.s3 import S3ClientNotInitializedException
from schemas.s3_client_config import S3ClientConfig


class S3Helper:
    def __init__(self, config: S3ClientConfig) -> None:
        self._config = config
        self.session: aioboto3.Session = aioboto3.Session()
        self._client: S3Client | None = None

    async def connect(self) -> None:
        if self._client is not None:
            return
        self._client = await self.session.client("s3", **self._config.model_dump()).__aenter__()

    async def close(self) -> None:
        if self._client is None:
            return
        await self._client.__aexit__(None, None, None)
        self._client = None

    def get_client(self) -> S3Client:
        if self._client is None:
            raise S3ClientNotInitializedException()
        return self._client


s3_helper = S3Helper(
    S3ClientConfig(
        endpoint_url=str(settings.s3.endpoint_url),
        aws_access_key_id=settings.s3.access_key,
        aws_secret_access_key=settings.s3.secret_key,
        region_name=settings.s3.region
    )
)
