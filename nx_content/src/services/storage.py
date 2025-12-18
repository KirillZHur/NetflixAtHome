import asyncio
from typing import AsyncGenerator

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from fastapi import HTTPException
from loguru import logger

from core.config import S3_CONFIG
from db.s3 import get_s3_client
from services.abstract_models import ServiceManager


class S3StreamingService:
    def __init__(self, storage: BaseClient | None):
        self.storage = storage
        self.bucket = S3_CONFIG["bucket"]
        self.chunk_size = S3_CONFIG["chunk_size"]

    async def _get_client(self) -> BaseClient:
        if not self.storage:
            raise HTTPException(
                status_code=503, detail="S3 client is not initialized yet"
            )
        return self.storage

    async def stream_file(
        self, key: str
    ) -> tuple[AsyncGenerator[bytes, None], str, int | None]:
        client = await self._get_client()

        try:
            response = await asyncio.to_thread(
                client.get_object,
                Bucket=self.bucket,
                Key=key,
            )
        except ClientError as err:
            error_code = err.response.get("Error", {}).get("Code")

            if error_code in ("NoSuchKey", "NoSuchBucket", "404"):
                raise HTTPException(status_code=404, detail="File not found") from err

            logger.exception(
                "Failed to fetch %s from bucket %s: %s", key, self.bucket, error_code
            )
            raise HTTPException(
                status_code=503, detail="Storage is temporarily unavailable"
            ) from err
        except Exception as err:
            logger.exception("Unexpected storage error for %s: %s", key, err)
            raise HTTPException(
                status_code=503, detail="Storage is temporarily unavailable"
            ) from err

        body = response["Body"]
        content_type = response.get("ContentType") or "application/octet-stream"
        content_length = response.get("ContentLength")

        async def file_iterator() -> AsyncGenerator[bytes, None]:
            try:
                while True:
                    chunk = await asyncio.to_thread(body.read, self.chunk_size)
                    if not chunk:
                        break
                    yield chunk
            finally:
                await asyncio.to_thread(body.close)

        return file_iterator(), content_type, content_length


s3_streaming_service = ServiceManager(S3StreamingService, get_s3_client)

