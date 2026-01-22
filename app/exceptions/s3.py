class S3Exception(Exception):
    pass


class S3ClientException(S3Exception):
    pass


class S3ClientNotInitializedException(S3ClientException):
    def __init__(self) -> None:
        super().__init__("S3 Client is not initialized. Call connect() inside lifespan or startup event.")


class S3UploadException(S3Exception):
    def __init__(self, obj_name: str) -> None:
        self.obj_name = obj_name
        super().__init__(f"Failed to update file {obj_name}.")


class S3DeleteException(S3Exception):
    def __init__(self, obj_name: str) -> None:
        self.obj_name = obj_name
        super().__init__(f"Failed to delete file {obj_name}.")
