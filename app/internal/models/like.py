from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .record import Record


class Like(Record):
    __tablename__ = "like"

    entity_id = Column(Integer, ForeignKey("likeable_entity.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="likes", uselist=False)
    post = relationship("Post", back_populates="likes", uselist=False)
