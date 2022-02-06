from sqlalchemy import Column, ForeignKey, Integer, String

from .record import Record


class PostImage(Record):
    __tablename__ = "post_image"

    post_id = Column(Integer, ForeignKey("post.id"))
    image_url = Column(String, nullable=False)
