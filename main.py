import uvicorn
from fastapi import FastAPI
from app.src.endpoints import files, buckets
from app.src.logger import setup_logger


app = FastAPI()

app.include_router(files.router)
app.include_router(buckets.router)

logger = setup_logger()


@app.get("/")
def ready_status():
    return {"message": "MinIO Interaction Service is running"}


if __name__ == "__main__":
    logger.info("Starting minio-api-service...")
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True, log_config=None)
