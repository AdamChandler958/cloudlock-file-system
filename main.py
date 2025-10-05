from minio import Minio
from dotenv import load_dotenv
import os

load_dotenv("dev.env")

MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
MINIO_ENDPOINT = "minio:9000"


client = Minio(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

bucket_list = client.list_buckets()
print(bucket_list)
