from functools import lru_cache

from pydantic import BaseSettings, validator, PostgresDsn



class Settings(BaseSettings):
    """Конфигурация проекта"""

    app_name: str
    app_domain: str
    # Debug
    debug: bool
    db_log_echo: bool

    # Postgres config
    db_name: str
    db_user: str
    db_host: str
    db_port: str
    db_password: str
    db_url: str = None
    db_dsn: str = None

    @validator("db_url", pre=True)
    def assemble_db_url(cls, v, values):
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            host=values.get("db_host"),
            port=values.get("db_port"),
            user=values.get("db_user"),
            password=values.get("db_password"),
        )

    @validator("db_dsn", pre=True)
    def assemble_db_dsn(cls, v, values):
        return values.get("db_url") + "/" + values.get("db_name")

    class Config:
        env_file = ".env"


@lru_cache
def _get_settings(**kwargs) -> Settings:
    return Settings(**kwargs)


settings = _get_settings()
