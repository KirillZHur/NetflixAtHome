from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    admin_postgres_db: str
    admin_postgres_user: str
    admin_postgres_password: str
    admin_postgres_host: str
    admin_postgres_port: int

    redis_host: str
    redis_port: int

    elastic_host: str
    elastic_port: int
