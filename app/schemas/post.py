from typing import List

from pydantic import AnyHttpUrl, BaseModel


class Post(BaseModel):
    image_urls: List[AnyHttpUrl]
    inital_caption: str
