from typing import Optional, Type

from app.auth.models import InstagramUser
from sqlalchemy.orm import Session

from .models import Comment, Like, LikeableEntity, Post, PostCreate


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


def get_comment(db: Session, current_post: Post, comment_id: int) -> Optional[Comment]:
    return db.query(Post).filter(Post.comments.any(comment_id=comment_id)).one_or_none()


def like_post_or_comment(
    db: Session, current_user: InstagramUser, current_entity: LikeableEntity
) -> None:
    # a user can only like a post/comment once
    if (
        db.query(InstagramUser)
        .filter(InstagramUser.likes.any(entity_id=current_entity.id))
        .count()
        == 0
    ):
        db.add(Like(entity_id=current_entity.id, user_id=current_user.id))
        db.commit()


def dislike_post_or_comment(
    db: Session, current_entity: LikeableEntity, current_user: InstagramUser
) -> None:
    db.query(Like).filter(Like.entity_id == current_entity.id).filter(
        Like.user_id == current_user.id
    ).delete()
    db.commit()
