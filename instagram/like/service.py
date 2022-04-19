from typing import List, Optional, Type

from instagram.post.models import LikeableEntity, Post, PostCreate
from instagram.user import service as user_service
from instagram.user.models import InstagramUser
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import Like


def add_user_meta(db: Session, like: Like, viewing_user: InstagramUser) -> None:
    user_service.add_user_meta(db=db, user=like.user, viewing_user=viewing_user)


def get_likeable(db: Session, likeable_id: int) -> LikeableEntity | None:
    return (
        db.query(LikeableEntity).filter(LikeableEntity.id == likeable_id).one_or_none()
    )


def create(db: Session, current_user: InstagramUser, likeable: LikeableEntity):
    try:
        db.add(Like(entity_id=likeable.id, user_id=current_user.id))
        db.commit()
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            db.rollback()
            print(
                f"user {current_user.id} has already liked {type(likeable).__name__} {likeable.id}"
            )
        else:
            raise


def get_all(db: Session, likeable_id: int, current_user: InstagramUser) -> List[Like]:
    likes = db.query(Like).filter(Like.entity_id == likeable_id).all()
    for like in likes:
        add_user_meta(db=db, like=like, viewing_user=current_user)

    return likes


def delete(db: Session, likeable: LikeableEntity, current_user: InstagramUser) -> None:
    like = (
        db.query(Like)
        .filter(Like.entity_id == likeable.id)
        .filter(Like.user_id == current_user.id)
        .one_or_none()
    )

    if like:
        db.delete(like)
        db.commit()
