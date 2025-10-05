from fastapi import APIRouter, Depends, HTTPException
from app.src.minio_client import get_client
from typing import Annotated
from minio import Minio
from app.src.models.BucketInfo import BucketInfo

router = APIRouter(prefix="/buckets", tags=["buckets", "storage"])


@router.get("/")
def list_files(client: Annotated[Minio, Depends(get_client)]):
    return client.list_buckets()


@router.post("/create_bucket/")
def create_bucket(
    bucket_info: BucketInfo, client: Annotated[Minio, Depends(get_client)]
):
    try:
        client.make_bucket(
            bucket_name=bucket_info.bucket_name,
            location=None,
            object_lock=bucket_info.object_lock,
        )
    except Exception as e:
        raise HTTPException(422, f"Making bucket failed with exception: {e}")

    return {"message": f"Bucket {bucket_info.bucket_name} created successfully"}
