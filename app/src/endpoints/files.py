from fastapi import APIRouter, Depends, UploadFile
from app.src.minio_client import get_client
from typing import Annotated
import os

from minio import Minio

router = APIRouter(prefix="/files", tags=["files", "storage"])


@router.post("/upload/{bucket_name}")
def single_file_upload(
    bucket_name: str, file: UploadFile, client: Annotated[Minio, Depends(get_client)]
):
    file_object = file.file
    object_name = file.filename

    file_object.seek(0, os.SEEK_END)
    file_size = file_object.tell()
    file_object.seek(0)

    try:
        result = client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=file_object,
            length=file_size,
            content_type=file.content_type,
        )
        return {
            "filename": file.filename,
            "minio_object_name": result.object_name,
            "etag": result.etag,
        }
    except Exception as e:
        return {"error": str(e)}
