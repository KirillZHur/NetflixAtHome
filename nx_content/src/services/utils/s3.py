from __future__ import annotations

from urllib.parse import quote_plus, urljoin

from core.config import S3_CONFIG


def build_s3_url(key: str | None) -> str | None:
    if not key:
        return None

    endpoint = S3_CONFIG.get("public_endpoint_url") or S3_CONFIG["endpoint_url"]
    bucket = S3_CONFIG["bucket"]

    base = endpoint if endpoint.endswith("/") else endpoint + "/"
    return urljoin(base, f"{bucket}/{key}")


def build_stream_path(key: str | None) -> str | None:
    if not key:
        return None
    safe_key = quote_plus(key)
    return f"/content-service/api/v1/storage/stream?key={safe_key}"

