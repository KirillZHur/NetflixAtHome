from botocore.client import BaseClient

s3_client: BaseClient | None = None


async def get_s3_client() -> BaseClient | None:
    return s3_client


