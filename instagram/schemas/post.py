from typing import List

from pydantic import AnyHttpUrl

from .base import BaseModel
from .user import UserResponse


class PostImage(BaseModel):
    image_url: AnyHttpUrl


class Comment(BaseModel):
    id: int
    text: str
    user: UserResponse


class PostCreate(BaseModel):
    images: List[PostImage]
    inital_caption: str


class PostResponse(BaseModel):
    id: int
    images: List[PostImage]
    inital_caption: str
    user: UserResponse
    user_id: int
    comments: List[Comment]
