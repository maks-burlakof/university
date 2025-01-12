import logging
from datetime import timedelta
from functools import lru_cache

from django_instagram.config.environments import EnvType
from pydantic import SecretStr
from pydantic_settings import BaseSettings as PydanticBaseSettings


class BaseSettings(PydanticBaseSettings):
    env: EnvType
    debug: bool = False
    secret_key: SecretStr = SecretStr("secret")
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    allowed_hosts: list[str] = ["*"]
    allowed_origins: list[str] = [backend_url, frontend_url]
    log_level: int = logging.INFO
    access_token_lifetime: timedelta = timedelta(minutes=15)
    refresh_token_lifetime: timedelta = timedelta(days=30)
    database_hostname: str = "postgres"
    database_port: int = "5432"
    database_name: str = "babushka"
    database_username: str = "postgres"
    database_password: SecretStr = SecretStr("postgres")
    s3_access_key_id: SecretStr
    s3_secret_access_key: SecretStr
    s3_region_name: str
    s3_endpoint_url: str
    s3_bucket_name: str

    class Config:
        env_file = ".env"
        extra = "ignore"


class TestSettings(BaseSettings):
    env: EnvType = EnvType.test
    debug: bool = True
    log_level: int = logging.ERROR


class LocalSettings(BaseSettings):
    env: EnvType = EnvType.local
    secret_key: SecretStr = SecretStr("rpWV7qx8Bal7aSW5FM2FjaAjRJIc0yXVZuMNtiScgk")
    database_hostname: str = "localhost"


class DevSettings(BaseSettings):
    env: EnvType = EnvType.dev
    debug: bool = True
    secret_key: SecretStr = SecretStr("rpWV7qx8Bal7aSW5FM2FjaAjRJIc0yXVZuMNtiScgk")


class ProdSettings(BaseSettings):
    env: EnvType = EnvType.prod


settings_mapping = {
    EnvType.dev: DevSettings,
    EnvType.test: TestSettings,
    EnvType.prod: ProdSettings,
    EnvType.local: LocalSettings,
}


@lru_cache
def get_settings() -> BaseSettings:
    app_env = BaseSettings().env
    return settings_mapping[app_env]()
