from fastapi import APIRouter, Depends
from app.src.minio_client import get_client
from typing import Annotated

from minio import Minio

router = APIRouter(prefix="/files", tags=["files", "storage"])


@router.get("/")
def list_files(client: Annotated[Minio, Depends(get_client)]):
    return client.list_buckets()
