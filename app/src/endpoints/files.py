from fastapi import APIRouter, Depends, UploadFile
from app.src.minio_client import get_client
from typing import Annotated

from minio import Minio

router = APIRouter(prefix="/files", tags=["files", "storage"])

# @router.post("/upload")
# def single_file_upload(file: UploadFile, client: Annotated[Minio, Depends(get_client)]):
#     client.
