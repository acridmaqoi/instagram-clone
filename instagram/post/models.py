from datetime import datetime
from sqlite3 import Date
from turtle import back
from typing import List

from instagram.comment.models import CommentRead
from instagram.database.core import Base, SessionLocal
from instagram.like.models import Like, LikeableEntity
from instagram.models import InstagramBase, user_context
from instagram.save.models import Save
from instagram.user.models import InstagramUser, UserReadSimple
from pydantic import BaseModel, Field, HttpUrl, root_validator, validator
from sqlalchemy import (
    TIMESTAMP,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    and_,
    delete,
    event,
    func,
    true,
)
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import and_, true

db = SessionLocal()


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
    saves = relationship("Save", cascade="all,delete", back_populates="post")
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


class CommentCreate(InstagramBase):
    text: str


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
    has_liked: bool = False
    has_saved: bool = False

    @validator("has_liked", always=True)
    def calc_has_liked(cls, v, values):
        try:
            post = db.query(Post).filter(Post.id == values["id"]).one()

            return (
                db.query(InstagramUser.has_liked(post))
                .filter(InstagramUser.id == user_context.get().id)
                .scalar()
            )

        except Exception as e:
            return v

    @validator("has_saved", always=True)
    def calc_has_saved(cls, v, values):
        try:
            return (
                db.query(Post.is_saved_by(user_context.get()))
                .filter(Post.id == values["id"])
                .scalar()
            )
        except Exception as e:
            return v


class PostReadList(InstagramBase):
    posts: List[PostRead]
    count: int


class PostCreate(PostBase):
    ...
