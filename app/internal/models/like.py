from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .record import Record


class Like(Record):
    __tablename__ = "like"

    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="likes", uselist=False)
    post = relationship("Post", back_populates="likes", uselist=False)
