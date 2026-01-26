from core.config import settings
from storage.abc import FileUrlResolverABC


class FileUrlResolver(FileUrlResolverABC):
    def __init__(self) -> None:
        self.base_url = f"{settings.s3.endpoint_url}{settings.s3.bucket_name}"

    def to_url(self, path: str) -> str:
        return f"{self.base_url}/{path}"

    def from_url(self, url: str) -> str:
        return url.removeprefix(self.base_url)
