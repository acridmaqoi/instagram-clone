from datetime import datetime

from instagram.database.core import Base, SessionLocal
from instagram.like.models import Like, LikeableEntity
from instagram.models import InstagramBase, TimeStampMixin, user_context
from instagram.user.models import UserReadSimple
from pydantic import root_validator
from sqlalchemy import Column, ForeignKey, Integer, String, orm
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

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
    has_liked: bool
    user: UserReadSimple

    @root_validator
    def has_liked(cls, values):
        try:
            if user_context.get():
                values["has_liked"] = (
                    db.query(Like)
                    .filter(Like.entity_id == values["id"])
                    .filter(Like.user_id == user_context.get())
                    .one_or_none()
                    is not None
                )
        except:
            pass
        return values


CommentRead.__post_root_validators__.reverse()
