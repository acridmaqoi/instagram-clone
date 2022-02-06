from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .record import Record


class Post(Record):
    __tablename__ = "post"

    inital_caption = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    image_urls = relationship("PostImage")
    comments = relationship("Comment")
