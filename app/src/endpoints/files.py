from fastapi import APIRouter, Depends, UploadFile, HTTPException
from app.src.minio_client import get_client
from typing import Annotated
import os

from app.src.logger import setup_logger

from minio import Minio

router = APIRouter(prefix="/files", tags=["files", "storage"])

logger = setup_logger()


@router.post("/upload/{bucket_name}")
def single_file_upload(
    bucket_name: str, file: UploadFile, client: Annotated[Minio, Depends(get_client)]
):
    logger.info(f"Received request to upload an object to bucket {bucket_name}")
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
        logger.error(f"An error occured during file upload: {e}")
        return {"error": str(e)}


@router.delete("/delete/{bucket_name}")
def single_file_delete(
    bucket_name: str, object_name: str, client: Annotated[Minio, Depends(get_client)]
):
    logger.info(
        f"Received request to delete object {object_name} from bucket {bucket_name}."
    )
    if client.get_object(bucket_name, object_name) is not None:
        try:
            client.remove_object(bucket_name, object_name)
        except Exception as e:
            logger.error(f"An error occured while removing object: {e}")
            raise HTTPException(422, f"An error occured while removing object: {e}")
    else:
        logger.error(f"Object {object_name} does not exist")
        raise HTTPException(404, f"Object {object_name} does not exist")

    logger.info(f"Object {object_name} deleted from bucket {bucket_name} successfully.")
    return {
        "message": f"Object {object_name} deleted from bucket {bucket_name} successfully"
    }


@router.get("/files")
def get_files_in_bucket(
    bucket_name: str, client: Annotated[Minio, Depends(get_client)]
):
    logger.info(f"Received request to list files in bucket {bucket_name}.")
    bucket_list = client.list_objects(bucket_name=bucket_name, recursive=True)
    return bucket_list


@router.delete("/delete_all/{bucket_name}")
def recurssive_delete_objects(
    bucket_name: str, client: Annotated[Minio, Depends(get_client)]
):
    logger.info(f"Received request to purge all objects from bucket {bucket_name}.")
    bucket_list = get_files_in_bucket(bucket_name, client)
    for obj in bucket_list:
        single_file_delete(
            bucket_name=bucket_name, object_name=obj.object_name, client=client
        )

    logger.info(f"All objects in {bucket_name} deleted successfully")

    return {"message": f"All items in {bucket_name} deleted successfully."}
