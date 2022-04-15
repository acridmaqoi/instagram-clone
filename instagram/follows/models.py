from instagram.database.core import Base
from instagram.models import BaseModel
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Follow(Base):
    from_user_id = Column(Integer, ForeignKey("instagram_user.id"), primary_key=True)
    to_user_id = Column(Integer, ForeignKey("instagram_user.id"), primary_key=True)

    __table_args__ = (
        CheckConstraint(
            "from_user_id <> to_user_id", name="from_user_to_user_cannot_be_equal"
        ),
    )

    from_user = relationship(
        "InstagramUser",
        uselist=False,
        back_populates="following_follows",
        foreign_keys="Follow.from_user_id",
    )

    to_user = relationship(
        "InstagramUser",
        uselist=False,
        back_populates="followers_follows",
        foreign_keys="Follow.to_user_id",
    )
