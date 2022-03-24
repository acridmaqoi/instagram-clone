from fastapi import APIRouter, Body, Depends, HTTPException, status
from instagram.user.models import InstagramUser
from instagram.user.service import get_current_user
from instagram.database.core import get_db
from sqlalchemy.orm import Session

from .models import Comment, Post, PostCreate, PostRead
from .service import (
    add_comment,
    create,
    delete,
    dislike_post_or_comment,
    get,
    get_comment,
    like_post_or_comment,
    uncomment,
)

router = APIRouter(prefix="/posts", tags=["posts"])


def get_current_post(post_id: int, db: Session = Depends(get_db)):
    post = get(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={post_id} not found",
        )
    return post


@router.post("", response_model=PostRead)
def create_post(
    post_in: PostCreate,
    user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create(db=db, post_in=post_in, user_id=user.id)


@router.get("/{post_id}", response_model=PostRead)
def get_post(post: Post = Depends(get_current_post), db: Session = Depends(get_db)):
    return post


@router.delete("/{post_id}")
def delete_post(
    current_post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != current_post.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    delete(db=db, post_id=current_post.id)
