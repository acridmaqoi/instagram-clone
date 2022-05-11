from typing import List, Optional, Type

from instagram.comment import service as comment_service
from instagram.comment.models import Comment
from instagram.user.models import InstagramUser
from sqlalchemy.orm import Session

from .models import Image, LikeableEntity, Post, PostCreate


def create(db: Session, post_in: PostCreate, current_user: InstagramUser) -> Post:
    post = Post(
        caption=post_in.caption,
        images=[Image(url=image.url) for image in post_in.images],
        user_id=current_user.id,
    )
    db.add(post)
    db.commit()

    return post


def get(db: Session, current_user: InstagramUser, post_id: int) -> Optional[Post]:
    post = db.query(Post).filter(Post.id == post_id).one_or_none()

    return post


def get_all_for_user(
    db: Session, current_user: InstagramUser, user_id: int, exclude_posts_ids: List[int]
) -> List[Post]:
    posts = (
        db.query(Post)
        .filter(Post.user_id == user_id)
        .filter(Post.id.not_in([id for id in exclude_posts_ids]))
        .all()
    )

    return posts


def delete(db: Session, post_id: int) -> None:
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()
