from typing import List, Optional, Type

from instagram.user.models import InstagramUser
from sqlalchemy.orm import Session

from .models import Comment, Image, Like, LikeableEntity, Post, PostCreate


def add_user_meta(post: Post, current_user: InstagramUser) -> None:
    post.has_liked = next(
        (True for like in post.likes if like.user_id == current_user.id), False
    )
    post.has_saved = next(
        (True for save in current_user.saved_posts if save.post_id == post.id),
        False,
    )


def create(db: Session, post_in: PostCreate, current_user: InstagramUser) -> Post:
    post = Post(
        caption=post_in.caption,
        images=[Image(url=image.url) for image in post_in.images],
        user_id=current_user.id,
    )
    db.add(post)
    db.commit()

    add_user_meta(post=post, current_user=current_user)
    return post


def get(db: Session, current_user: InstagramUser, post_id: int) -> Optional[Post]:
    post = db.query(Post).filter(Post.id == post_id).one_or_none()
    if post:
        add_user_meta(post=post, current_user=current_user)

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
    for post in posts:
        add_user_meta(post=post, current_user=current_user)

    return posts


def delete(db: Session, post_id: int) -> None:
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()


def get_comment(db: Session, current_post: Post, comment_id: int) -> Optional[Comment]:
    return (
        db.query(Comment)
        .filter(Comment.post_id == current_post.id)
        .filter(Comment.id == comment_id)
        .one_or_none()
    )


def add_comment(
    db: Session, current_post: Post, comment: str, current_user: InstagramUser
) -> None:
    current_post.comments.append(Comment(text=comment, user_id=current_user.id))
    db.commit()


def uncomment(db: Session, current_post: Post, comment_id: int):
    db.query(Comment).filter(Comment.post_id == current_post.id).filter(
        Comment.id == comment_id
    ).delete()
    db.commit()


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
