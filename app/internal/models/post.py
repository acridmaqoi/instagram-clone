from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .record import Record


class Post(Record):
    __tablename__ = "posts"

    inital_caption = Column(String, nullable=False)
    image_urls = relationship("PostImage")
