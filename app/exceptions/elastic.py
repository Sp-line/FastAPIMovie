class ElasticException(Exception):
    pass


class ElasticClient(ElasticException):
    pass


class ElasticClientNotInitializedException(ElasticClient):
    def __init__(self) -> None:
        super().__init__("Elastic Client is not initialized. Call connect() inside lifespan or startup event.")


class ElasticConnectionFailed(ElasticException):
    def __init__(self) -> None:
        super().__init__("Elastic Connection failed.")