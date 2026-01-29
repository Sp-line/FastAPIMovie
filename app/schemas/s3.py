from pydantic import BaseModel


class S3ClientConfig(BaseModel):
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str  = "us-east-1"