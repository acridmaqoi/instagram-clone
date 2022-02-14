from typing import Optional

from sqlalchemy.orm import Session

from .models import Post, PostCreate


def create(db: Session, post_in: PostCreate, user_id=int) -> Post:
    post = Post(**post_in.dict(), user_id=user_id)
    db.add(post)
    db.commit()
    return post


def get(db: Session, post_id: int) -> Optional[Post]:
    return db.query(Post).filter(Post.id == post_id).one_or_none()


def delete(db: Session, post_id: int) -> None:
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()
