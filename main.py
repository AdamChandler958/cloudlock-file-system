from minio import Minio
from dotenv import load_dotenv
import os
import uvicorn
from fastapi import FastAPI

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

app = FastAPI()


@app.get("/")
def ready_status():
    return {"message": "MinIO Interaction Service is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
