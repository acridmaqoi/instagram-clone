from app.internal.models import post
from app.internal.models.comment import Comment
from app.schemas.post import PostCreate, PostResponse
from sqlalchemy.orm import Session

from ..models.like import Like
from ..models.post import Post
from ..models.user import User
from . import record_crud
from .record_crud import RecordNotFound


def get_post_by_id(db: Session, post_id: int):
    return record_crud.get_record_by_id(db=db, id=post_id, model=Post)


def create_post(db: Session, post: PostCreate, user_id: int):
    return record_crud.write_record(db=db, record=Post(**post.dict(), user_id=user_id))


def delete_post(db: Session, post_id: int):
    return record_crud.delete_record_by_id(db=db, id=post_id, model=Post)


def like_post(db: Session, post_id: int, user: User):
    # user can only like a post once
    if user.likes.filter(Like.post_id == post_id).count() == 0:
        user.likes.append(Like(post_id=post_id))
        db.commit()


def dislike_post(db: Session, post_id: int, user: User):
    user.likes.filter(Like.post_id == post_id).delete()
    db.commit()


def create_post_comment(db: Session, post_id: int, user: User, comment: str):
    post = record_crud.get_record_by_id(db=db, id=post_id, model=Post)

    comment = Comment(text=comment, user_id=user.id)
    post.comments.append(comment)

    db.commit()
    return comment


def delete_post_comment(db: Session, post_id: int, comment_id: int):
    post = record_crud.get_record_by_id(db=db, id=post_id, model=Post)
    post.comments.filter(Comment.id == comment_id).delete()
    db.commit()


def get_post_comment(db: Session, post_id: int, comment_id: int):
    post = record_crud.get_record_by_id(db=db, id=post_id, model=Post)

    comment = post.comments.filter(Comment.id == comment_id).one_or_none()
    if comment is None:
        raise RecordNotFound(Comment, col="id", val=comment_id)

    return comment
