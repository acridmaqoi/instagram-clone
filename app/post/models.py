from app.database.core import Base
from app.models import InstagramBase
from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String


class Post(Base):
    id = Column(Integer, primary_key=True)
    caption = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("instagram_user.id"))


class PostBase(InstagramBase):
    caption: str


class PostRead(PostBase):
    id: int


class PostCreate(PostBase):
    ...
