from typing import AsyncIterable

from dishka import provide, Provider, Scope
from elasticsearch import AsyncElasticsearch
from redis.asyncio.client import Redis
from types_aiobotocore_s3 import S3Client

from cache import redis_helper
from core.models import db_helper
from elastic.elasticsearch import es_helper
from signals.event_session import EventSession
from storage.s3 import s3_helper


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def get_redis(self) -> Redis:
        return redis_helper.get_client()

    @provide(scope=Scope.APP)
    def get_elastic(self) -> AsyncElasticsearch:
        return es_helper.get_client()

    @provide(scope=Scope.REQUEST)
    def get_s3_client(self) -> S3Client:
        return s3_helper.get_client()

    @provide(scope=Scope.REQUEST)
    async def get_db_session(self) -> AsyncIterable[EventSession]:
        async with db_helper.session_factory() as session:
            yield session
