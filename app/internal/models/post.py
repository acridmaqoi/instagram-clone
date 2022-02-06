from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import object_session, relationship

from .record import Record


class Post(Record):
    __tablename__ = "post"

    inital_caption = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    images = relationship("PostImage")
    comments = relationship("Comment", back_populates="post")
