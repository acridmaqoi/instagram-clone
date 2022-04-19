from typing import List, Optional, Type

from instagram.post.models import LikeableEntity, Post, PostCreate
from instagram.user.models import InstagramUser
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import Like


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


def get_all(db: Session, likeable_id: int) -> List[Like]:
    return db.query(Like).filter(Like.entity_id == likeable_id).all()


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
