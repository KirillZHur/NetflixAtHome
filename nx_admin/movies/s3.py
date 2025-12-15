import uuid
import boto3
from django.conf import settings


def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=settings.MINIO_ENDPOINT_URL,
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        region_name='us-east-1',
    )

def _upload_file(file_obj, *, prefix: str):
    ext = file_obj.name.split('.')[-1].lower()
    key = f'{prefix}/{uuid.uuid4()}.{ext}'

    s3 = get_s3_client()
    s3.upload_fileobj(
        Fileobj=file_obj,
        Bucket=settings.MINIO_BUCKET_NAME,
        Key=key,
        ExtraArgs={
            'ContentType': file_obj.content_type,
        },
    )
    return key


def upload_video(file_obj):
    return _upload_file(file_obj, prefix='movies')


def upload_image(file_obj):
    idx = _upload_file(file_obj, prefix='images')
    print(idx)
    return idx
