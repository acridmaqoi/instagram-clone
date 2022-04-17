from datetime import datetime
from sqlite3 import Date
from turtle import back
from typing import List

from instagram.database.core import Base, SessionLocal
from instagram.like.models import LikeableEntity
from instagram.models import InstagramBase
from instagram.user.models import UserReadSimple
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import (
    TIMESTAMP,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    delete,
    event,
    func,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship


class Image(Base):
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))

    post = relationship("Post", uselist=False)


class Post(LikeableEntity):
    id = Column(Integer, ForeignKey("likeable_entity.id"), primary_key=True)
    caption = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("instagram_user.id"))
    posted_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    images = relationship("Image", cascade="all,delete", back_populates="post")
    user = relationship("InstagramUser", uselist=False, back_populates="posts")
    comments = relationship(
        "Comment",
        back_populates="post",
        foreign_keys="Comment.post_id",
        cascade="all,delete",
    )

    __mapper_args__ = {
        "polymorphic_identity": "post",
    }

    @hybrid_property
    def comment_count(self):
        return len(self.comments)


@event.listens_for(SessionLocal, "persistent_to_deleted")
def delete_likeable_entity(session, object_):
    # sqlalchemy doesn't support cascading polymorphic deletes
    if not isinstance(object_, LikeableEntity):
        return

    session.query(LikeableEntity).filter(LikeableEntity.id == object_.id).delete()


class Comment(LikeableEntity):
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


class CommentCreate(InstagramBase):
    text: str


class CommentRead(InstagramBase):
    id: int
    text: str
    user: UserReadSimple
    like_count: int


class ImageBase(InstagramBase):
    url: HttpUrl


class PostBase(InstagramBase):
    caption: str
    images: List[ImageBase]


class PostRead(PostBase):
    id: int
    user: UserReadSimple
    posted_at: datetime
    comments: List[CommentRead]
    like_count: int
    comment_count: int
    has_liked: bool
    has_saved: bool


class PostReadList(InstagramBase):
    posts: List[PostRead]
    count: int


class PostCreate(PostBase):
    ...
