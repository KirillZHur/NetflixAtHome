from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from services.storage import S3StreamingService, s3_streaming_service

router = APIRouter()


@router.get(
    "/stream",
    summary="Потоковая выдача файла из S3",
    description=(
        "Возвращает файл из S3 по его ключу"
    ),
)
async def stream_from_s3(
    key: str = Query(..., description="Ключ файла в бакете"),
    service: S3StreamingService = Depends(s3_streaming_service.get_service),
):
    stream, content_type, content_length = await service.stream_file(key)

    headers = {}
    if content_length:
        headers["Content-Length"] = str(content_length)

    return StreamingResponse(stream, media_type=content_type, headers=headers)


