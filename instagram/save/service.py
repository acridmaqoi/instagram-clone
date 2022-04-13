from typing import List

from instagram.post.models import Post
from instagram.user.models import InstagramUser
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import Save


def create(db: Session, post: Post, current_user: InstagramUser) -> None:
    try:
        db.add(Save(post_id=post.id, user_id=current_user.id))
        db.commit()
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            db.rollback()
            print(f"user {current_user.id} has already saved post {post.id}")
        else:
            raise


def get_all_posts(db: Session, user: InstagramUser) -> List[Post | None]:
    from instagram.post import service as post_service

    saves = db.query(Save).filter(Save.user_id == user.id).all()
    return [
        post_service.get(db=db, post_id=save.post_id, current_user=user)
        for save in saves
    ]


def delete(db: Session, post: Post, current_user: InstagramUser) -> None:
    db.query(Save).filter(Save.post_id == post.id).filter(
        Save.user_id == current_user.id
    ).delete()
    db.commit()
