from app.internal.models.likeable_entity import Comment, Like, Post
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..internal.controllers import post_controller
from ..internal.database import get_db
from ..internal.models.post_image import PostImage
from ..internal.models.user import User
from ..schemas.post import Comment, PostCreate, PostResponse

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


@router.post("/{post_id}/likes")
def like_post(
    post_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post_controller.like_post(db=db, post_id=post_id, user=user)

    return {"ok": True}


@router.delete("/{post_id}/likes")
def unlike_post(
    post_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post_controller.dislike_post(db=db, post_id=post_id, user=user)

    return {"ok": True}


@router.post("/{post_id}/comments", response_model=Comment)
def create_post_comment(
    post_id: int,
    text: str = Body(..., embed=True),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return post_controller.create_post_comment(
        db=db, comment=text, post_id=post_id, user=user
    )


@router.delete("/{post_id}/comments/{comment_id}")
def delete_post_comment(
    post_id: int,
    comment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comment = post_controller.get_post_comment(
        db=db, comment_id=comment_id, post_id=post_id
    )
    if comment.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    post_controller.delete_post_comment(db=db, post_id=post_id, comment_id=comment_id)

    return {"ok": True}
