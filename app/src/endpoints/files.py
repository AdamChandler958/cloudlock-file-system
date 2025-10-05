from fastapi import APIRouter, Depends, UploadFile, HTTPException
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


@router.delete("/delete/{bucket_name}")
def single_file_delete(
    bucket_name: str, object_name: str, client: Annotated[Minio, Depends(get_client)]
):
    if client.get_object(bucket_name, object_name) is not None:
        try:
            client.remove_object(bucket_name, object_name)
        except Exception as e:
            raise HTTPException(422, f"An error occured while removing object: {e}")
    else:
        raise HTTPException(404, f"Object {object_name} does not exist")

    return {
        "message": f"Object {object_name} deleted from bucket {bucket_name} successfully"
    }


@router.get("/files")
def get_files_in_bucket(
    bucket_name: str, client: Annotated[Minio, Depends(get_client)]
):
    bucket_list = client.list_objects(bucket_name=bucket_name, recursive=True)
    return bucket_list


@router.delete("/delete_all/{bucket_name}")
def recurssive_delete_objects(
    bucket_name: str, client: Annotated[Minio, Depends(get_client)]
):
    bucket_list = get_files_in_bucket(bucket_name, client)
    for obj in bucket_list:
        single_file_delete(
            bucket_name=bucket_name, object_name=obj.object_name, client=client
        )

    return {"message": f"All items in {bucket_name} deleted successfully."}
