import logging

from nats.js.api import RetentionPolicy, DiscardPolicy
from pydantic import BaseModel, HttpUrl, PostgresDsn, AmqpDsn, NatsDsn, RedisDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from log import LogLevel


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class GunicornConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    timeout: int = 900


class LoggingConfig(BaseModel):
    log_level: LogLevel = "info"
    log_format: str = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    log_datefmt: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class TaskiqConfig(BaseModel):
    url: AmqpDsn
    log_format: str = "[%(asctime)s.%(msecs)03d][%(processName)s] %(module)16s:%(lineno)-3d %(levelname)-7s - %(message)s"


class FastStreamConfig(BaseModel):
    nats_url: NatsDsn


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class S3Config(BaseModel):
    endpoint_url: HttpUrl
    access_key: str
    secret_key: str
    bucket_name: str
    region: str


class RedisConfig(BaseModel):
    url: RedisDsn


class ElasticsearchConfig(BaseModel):
    url: HttpUrl


class MetricsConfig(BaseModel):
    enabled: bool
    endpoint: str


class SentryConfig(BaseModel):
    dsn: HttpUrl


class OTLPConfig(BaseModel):
    enabled: bool
    service_name: str
    endpoint: str


class JStreamConfig(BaseModel):
    name: str = "catalog_stream"
    subjects: list[str] = ["catalog.>", ]
    retention: RetentionPolicy = RetentionPolicy.LIMITS
    max_age: int = 24 * 60 * 60
    discard: DiscardPolicy = DiscardPolicy.OLD


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore"
    )
    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()
    api: ApiPrefix = ApiPrefix()
    jstream: JStreamConfig = JStreamConfig()
    otlp: OTLPConfig
    sentry: SentryConfig
    metrics: MetricsConfig
    elasticsearch: ElasticsearchConfig
    redis: RedisConfig
    faststream: FastStreamConfig
    taskiq: TaskiqConfig
    db: DatabaseConfig
    s3: S3Config


settings = Settings()  # type: ignore[call-arg]
