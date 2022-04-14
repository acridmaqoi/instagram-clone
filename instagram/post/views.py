from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from instagram.database.core import get_db
from instagram.user.models import InstagramUser
from instagram.user.service import get_authenticated_user
from instagram.user.views import get_current_user
from sqlalchemy.orm import Session

from .models import Comment, Post, PostCreate, PostRead, PostReadList
from .service import (
    add_comment,
    create,
    delete,
    dislike_post_or_comment,
    get,
    get_all_for_user,
    get_comment,
    like_post_or_comment,
    uncomment,
)

router = APIRouter(prefix="/posts", tags=["posts"])


def get_current_post(
    post_id: int,
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    post = get(db=db, post_id=post_id, current_user=current_user)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={post_id} not found",
        )
    return post


@router.post("", response_model=PostRead)
def create_post(
    post_in: PostCreate,
    user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    return create(db=db, post_in=post_in, current_user=user)


@router.get("/{post_id}", response_model=PostRead)
def get_post(
    post: Post = Depends(get_current_post),
    db: Session = Depends(get_db),
):
    return post


@router.get("", response_model=PostReadList)
def get_all_posts_for_user(
    current_user: InstagramUser = Depends(get_current_user),
    authenticated_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    posts = get_all_for_user(user_id=current_user.id, current_user=current_user, db=db)
    return {"posts": posts, "count": len(posts)}


@router.delete("/{post_id}")
def delete_post(
    current_post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    if current_user.id != current_post.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    delete(db=db, post_id=current_post.id)
