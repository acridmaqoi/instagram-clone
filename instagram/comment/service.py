from instagram.post.models import CommentCreate, Post
from instagram.user.models import InstagramUser
from sqlalchemy.orm import Session

from .models import Comment


def create(
    db: Session,
    comment_in: CommentCreate,
    post: Post,
    current_user: InstagramUser,
):
    comment = Comment(text=comment_in.text, post_id=post.id, user_id=current_user.id)

    db.add(comment)
    db.commit()


def delete(db: Session, post_id: int, comment_id: int):
    comment = (
        db.query(Comment)
        .filter(Post.id == post_id)
        .filter(Comment.id == comment_id)
        .one_or_none()
    )

    if comment:
        db.delete(comment)
        db.commit()
