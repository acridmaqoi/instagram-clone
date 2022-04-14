from instagram.database.core import Base
from instagram.models import BaseModel
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Follow(Base):
    from_user_id = Column(Integer, ForeignKey("instagram_user.id"), primary_key=True)
    to_user_id = Column(Integer, ForeignKey("instagram_user.id"), primary_key=True)

    from_user = relationship(
        "InstagramUser",
        uselist=False,
        back_populates="following",
        foreign_keys="Follow.from_user_id",
    )

    to_user = relationship(
        "InstagramUser",
        uselist=False,
        back_populates="followers",
        foreign_keys="Follow.to_user_id",
    )
