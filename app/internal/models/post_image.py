from sqlalchemy import Column, ForeignKey, Integer, String

from .record import Record


class PostImage(Record):
    __tablename__ = "post_images"

    post_id = Column(Integer, ForeignKey("posts.id"))
    image_url = Column(String, nullable=False)
