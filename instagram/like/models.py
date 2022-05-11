from instagram.database.core import Base, SessionLocal
from instagram.models import InstagramBase
from instagram.user.models import InstagramUser, UserReadSimple
from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String, delete, event
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import and_, true


class LikeableEntity(Base):
    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    likes = relationship("Like")

    __mapper_args__ = {
        "polymorphic_identity": "likeable_entity",
        "polymorphic_on": type,
    }

    @hybrid_property
    def like_count(self):
        return len(self.likes)

    @hybrid_method
    def is_liked_by(self, user: InstagramUser):
        return any(like.user_id == user.id for like in self.likes)

    @is_liked_by.expression
    def is_liked_by(cls, user: InstagramUser):
        return and_(true(), cls.likes.any(user_id=user.id))


class Like(Base):
    entity_id = Column(
        Integer,
        ForeignKey("likeable_entity.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    user_id = Column(
        Integer, ForeignKey("instagram_user.id"), nullable=False, primary_key=True
    )

    user = relationship("InstagramUser", back_populates="likes", uselist=False)
    entity = relationship("LikeableEntity", back_populates="likes", uselist=False)
