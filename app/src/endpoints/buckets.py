from fastapi import APIRouter, Depends, HTTPException
from app.src.minio_client import get_client
from typing import Annotated
from minio import Minio
from app.src.models.BucketInfo import BucketInfo
from app.src.logger import setup_logger

from app.src.endpoints.files import get_files_in_bucket, recurssive_delete_objects

router = APIRouter(prefix="/buckets", tags=["buckets", "storage"])

logger = setup_logger()


@router.get("/")
def list_files(client: Annotated[Minio, Depends(get_client)]):
    logger.info("Received request to list all buckets.")
    return client.list_buckets()


@router.post("/create_bucket/")
def create_bucket(
    bucket_info: BucketInfo, client: Annotated[Minio, Depends(get_client)]
):
    logger.info(f"Received request to create bucket {bucket_info.bucket_name}.")
    try:
        client.make_bucket(
            bucket_name=bucket_info.bucket_name,
            location=None,
            object_lock=bucket_info.object_lock,
        )
    except Exception as e:
        logger.error(f"Making bucket failed with exception: {e}")
        raise HTTPException(422, f"Making bucket failed with exception: {e}")

    logger.info(f"Creation of bucket {bucket_info.bucket_name} successful.")
    return {"message": f"Bucket {bucket_info.bucket_name} created successfully"}


@router.delete("/delete_bucket")
def delete_bucket(bucket_name: str, client: Annotated[Minio, Depends(get_client)]):
    logger.info(f"Received request to delete bucket {bucket_name}")
    if client.bucket_exists(bucket_name=bucket_name):
        if get_files_in_bucket(bucket_name, client) is not None:
            recurssive_delete_objects(bucket_name, client)
        try:
            client.remove_bucket(bucket_name=bucket_name)
        except Exception as e:
            logger.error(f"An error occured while removing bucket: {e}")
            raise HTTPException(422, f"An error occured while removing bucket: {e}")
    else:
        logger.warning("Bucket does not exist")
        raise HTTPException(404, "Bucket does not exist.")

    logger.info(f"Bucket {bucket_name} deleted successfully")
    return {"message": f"Bucket {bucket_name} deleted successfully"}
