from starlette.config import Config

config = Config(".env")

SQLALCHEMY_DATABASE_URI = config(
    "SQLALCHEMY_DATABASE_URI",
    default="postgresql://postgres:password@localhost:5433/instagram",
)
S3_BUCKET_NAME = config("S3_BUCKET_NAME", default="instagram-static-123481")
