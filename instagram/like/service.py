from typing import Optional, Type

from profile.models import InstagramUser
from instagram.profile.models import InstagramUser
from post.models import Comment, Like, LikeableEntity, Post, PostCreate
from sqlalchemy.orm import Session


def create(db: Session, current_user: InstagramUser, current_post: Post):
    # a user can only like a post/comment once
    if (
        db.query(InstagramUser)
        .filter(InstagramUser.likes.any(entity_id=current_post.id))
        .count()
        == 0
    ):
        db.add(Like(entity_id=current_post.id, user_id=current_user.id))
        db.commit()


def delete(db: Session, current_user: InstagramUser, current_post: Post):
    db.query(Like).filter(Like.entity_id == current_post.id).filter(
        Like.user_id == current_user.id
    ).delete()
    db.commit()
