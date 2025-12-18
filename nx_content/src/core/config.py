import os
from logging import config as logging_config

from core.logger import LOGGING
from models.settings_model import NXBackendEnvSettings

settings = NXBackendEnvSettings()

REDIS_CONFIG = {
    "host": settings.redis_host,
    "port": settings.redis_port,
}

ES_CONFIG = {
    "host": settings.elastic_host,
    "port": settings.elastic_port,
}

AUTH_SERVICE_URL = settings.auth_service_url

S3_CONFIG = {
    "endpoint_url": settings.s3_endpoint_url,
    "public_endpoint_url": settings.s3_public_endpoint_url or settings.s3_endpoint_url,
    "access_key": settings.s3_access_key,
    "secret_key": settings.s3_secret_key,
    "bucket": settings.s3_bucket,
    "region": settings.s3_region or None,
    "secure": settings.s3_secure,
    "chunk_size": settings.s3_chunk_size,
}

PROJECT_NAME: str = "nx_backend"

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
