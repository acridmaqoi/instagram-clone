from datetime import datetime

from instagram.database.core import Base, SessionLocal
from instagram.like.models import Like, LikeableEntity
from instagram.models import InstagramBase, TimeStampMixin, user_context
from instagram.user.models import InstagramUser, UserReadSimple
from pydantic import BaseModel, Field, root_validator, validator
from sqlalchemy import Column, ForeignKey, Integer, String, delete, event, orm
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import and_, true

db = SessionLocal()


class Comment(LikeableEntity, TimeStampMixin):
    id = Column(Integer, ForeignKey("likeable_entity.id"), primary_key=True)
    text = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("instagram_user.id"), nullable=False)

    user = relationship("InstagramUser", uselist=False)

    post = relationship(
        "Post",
        back_populates="comments",
        uselist=False,
        foreign_keys="Comment.post_id",
    )

    __mapper_args__ = {
        "polymorphic_identity": "comment",
    }

    @orm.reconstructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.has_liked = False


class CommentCreate(InstagramBase):
    text: str


class CommentRead(CommentCreate):
    id: int
    created_at: datetime
    like_count: int
    user: UserReadSimple

    has_liked: bool = False

    @validator("has_liked", always=True)
    def calc_has_liked(cls, v, values):
        try:
            comment = db.query(Comment).filter(Comment.id == values["id"]).one()

            return (
                db.query(InstagramUser.has_liked(comment))
                .filter(InstagramUser.id == user_context.get().id)
                .scalar()
            )
        except LookupError as e:
            return v
