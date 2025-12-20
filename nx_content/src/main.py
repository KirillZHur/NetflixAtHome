import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

import boto3
from boto3 import session as boto3_session
from botocore.config import Config
from loguru import logger

import core.session as session
from aiohttp import ClientSession
from api.v1 import films, genres, persons, heartbeat, storage
from core.config import ES_CONFIG, PROJECT_NAME, REDIS_CONFIG, S3_CONFIG
from core.token import get_user_from_auth_service
from core.tracer import setup_tracer
from db import elastic, redis, s3
from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.elasticsearch import ElasticsearchInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis


setup_tracer()
AioHttpClientInstrumentor().instrument()
RedisInstrumentor().instrument()
ElasticsearchInstrumentor().instrument()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start content service!")
    session.aiohttp_session = ClientSession()
    redis.redis = Redis(**REDIS_CONFIG)
    elastic.es = AsyncElasticsearch(hosts=["{host}:{port}".format(**ES_CONFIG)])
    s3_session: boto3_session.Session = boto3.Session()
    s3.s3_client = s3_session.client(
        "s3",
        endpoint_url=S3_CONFIG["endpoint_url"],
        aws_access_key_id=S3_CONFIG["access_key"],
        aws_secret_access_key=S3_CONFIG["secret_key"],
        region_name=S3_CONFIG["region"],
        use_ssl=S3_CONFIG["secure"],
        config=Config(signature_version="s3v4"),
    )
    yield
    await session.aiohttp_session.close()
    session.aiohttp_session = None
    await redis.redis.close()
    await elastic.es.close()
    if s3.s3_client and hasattr(s3.s3_client, "close"):
        await asyncio.to_thread(s3.s3_client.close)
    s3.s3_client = None


app = FastAPI(
    title=PROJECT_NAME,
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FastAPIInstrumentor.instrument_app(app)

BASE_DIR = Path(__file__).resolve().parent
logger.remove()
logger.add(
    BASE_DIR / "nx_content.log",
    level="INFO",
    format="{message}",
    serialize=True,
)


api_router_main = APIRouter(
    prefix="/content-service", dependencies=[Depends(get_user_from_auth_service)]
)

api_router_v1 = APIRouter(prefix="/api/v1")

api_router_v1.include_router(films.router, prefix="/films", tags=["films"])
api_router_v1.include_router(genres.router, prefix="/genres", tags=["genres"])
api_router_v1.include_router(persons.router, prefix="/persons", tags=["persons"])
api_router_v1.include_router(storage.router, prefix="/storage", tags=["storage"])

api_router_main.include_router(api_router_v1)

app.include_router(api_router_main)
app.include_router(heartbeat.router)
