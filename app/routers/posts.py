from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..internal.controllers import post_controller
from ..internal.database import get_db
from ..internal.models.comment import Comment
from ..internal.models.like import Like
from ..internal.models.post import Post
from ..internal.models.post_image import PostImage
from ..internal.models.user import User
from ..schemas.post import PostCreate, PostResponse

router = APIRouter()


@router.post("", response_model=PostResponse)
def create_post(
    post: PostCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return post_controller.create_post(db=db, post=post, user_id=user.id)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = post_controller.get_post_by_id(db=db, post_id=post_id)
    return post


@router.delete("/{post_id}")
def delete_post(
    post_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    post = post_controller.get_post_by_id(db=db, post_id=post_id)
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    post_controller.delete_post(db=db, post_id=post_id)

    return {"ok": True}


@router.post("/{post_id}/comments")
def create_post_comment(
    post_id: int,
    text: str = Body(..., embed=True),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return Comment.create(db=db, text=text, post_id=post_id, user_id=user.id)


@router.delete("/{post_id}/comments/{comment_id}")
def delete_post_comment(
    post_id: int,
    comment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comment = Comment.get_by_id(db=db, id=comment_id)
    if comment.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    Post.get_by_id(db=db, id=post_id)
    Comment.delete_by_id(db=db, id=comment_id)

    return {"ok": True}


@router.post("/{post_id}/likes")
def like_post(
    post_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    Like.create(db=db, user_id=user.id, post_id=post_id)
    return {"ok": True}


@router.delete("/{post_id}/likes")
def unlike_post(
    post_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user.likes.filter(Like.post_id == post_id).delete()
    db.commit()
    return {"ok": True}
