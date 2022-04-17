from instagram.post.models import CommentCreate, Post
from instagram.user.models import InstagramUser
from sqlalchemy.orm import Session

from .models import Comment


def create(
    db: Session,
    comment_in: CommentCreate,
    post: Post,
    current_user: InstagramUser,
) -> None:
    comment = Comment(text=comment_in.text, post_id=post.id, user_id=current_user.id)

    db.add(comment)
    db.commit()


def get(db: Session, comment_id: int) -> Comment | None:
    return db.query(Comment).filter(Comment.id == comment_id).one_or_none()


def delete(db: Session, comment_id: int) -> None:
    comment = db.query(Comment).filter(Comment.id == comment_id).one_or_none()

    if comment:
        db.delete(comment)
        db.commit()
