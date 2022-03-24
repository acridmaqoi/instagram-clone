from uuid import uuid4

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException
from instagram import config
from instagram.user.service import get_authenticated_user

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/s3url")
def get_s3_url(current_user=Depends(get_authenticated_user)):
    s3 = boto3.client("s3", config=Config(signature_version="s3v4"))
    image_name = str(uuid4())

    try:
        url = s3.generate_presigned_url(
            "put_object",
            Params={"Bucket": str(config.S3_BUCKET_NAME), "Key": image_name},
            ExpiresIn=60,
        )
        return {"url": url}
    except ClientError as e:
        raise HTTPException(status_code=500, detail="error generating URL")
