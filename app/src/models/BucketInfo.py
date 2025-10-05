from pydantic import BaseModel


class BucketInfo(BaseModel):
    bucket_name: str
    location: str | None = None
    object_lock: bool = False
