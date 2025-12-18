from pydantic_settings import BaseSettings, SettingsConfigDict


class NXBackendEnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    redis_host: str
    redis_port: int

    elastic_host: str
    elastic_port: int

    auth_service_url: str

    s3_endpoint_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str
    s3_region: str | None = None
    s3_secure: bool = False
    s3_chunk_size: int = 1024 * 1024
    s3_public_endpoint_url: str | None = None
