from app.internal.models.like import Like
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .record import Record


class LikeableEntity(Record):
    __tablename__ = "likeable_entity"

    type = Column(String(50))
    likes = relationship("Like")

    __mapper_args__ = {
        "polymorphic_identity": "likeable_entity",
        "polymorphic_on": type,
    }


class Post(LikeableEntity):
    __tablename__ = "post"

    id = Column(Integer, ForeignKey("likeable_entity.id"), primary_key=True)
    inital_caption = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    images = relationship("PostImage")
    comments = relationship(
        "Comment", back_populates="post", foreign_keys="Comment.post_id"
    )

    _comments = relationship(
        "Comment", back_populates="post", lazy="dynamic", foreign_keys="Comment.post_id"
    )

    __mapper_args__ = {
        "polymorphic_identity": "post",
    }


class Comment(LikeableEntity):
    __tablename__ = "comment"

    id = Column(Integer, ForeignKey("likeable_entity.id"), primary_key=True)
    text = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    post = relationship(
        "Post",
        back_populates="comments",
        uselist=False,
        foreign_keys="Comment.post_id",
    )

    __mapper_args__ = {
        "polymorphic_identity": "comment",
    }
