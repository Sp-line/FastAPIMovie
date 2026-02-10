import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from core.config import settings


def setup_sentry() -> None:
    sentry_sdk.init(
        dsn=str(settings.sentry.dsn),
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
            RedisIntegration(),
            AioHttpIntegration(),
        ],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,

        send_default_pii=True,
    )