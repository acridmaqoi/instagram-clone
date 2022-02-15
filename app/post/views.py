from app.auth.models import InstagramUser
from app.auth.service import get_current_user
from app.database.core import get_db
from fastapi import APIRouter, Body, Depends, HTTPException, status
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


def get_current_comment(
    comment_id: int,
    current_post: Post = Depends(get_current_post),
    db: Session = Depends(get_db),
):
    comment = get_comment(db=db, current_post=current_post, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id={comment_id} not found",
        )
    return comment


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


@router.post("/{post_id}/comments")
def comment(
    comment: str = Body(..., embed=True),
    current_post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    add_comment(
        db=db, current_post=current_post, comment=comment, current_user=current_user
    )


@router.delete("/{post_id}/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comment = get_comment(db=db, current_post=current_post, comment_id=comment_id)
    if comment is None:
        raise HTTPException(404)
    if comment.user_id != current_user.id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    delete_comment(db=db, current_post=current_post, comment_id=comment_id)


@router.post("/{post_id}/likes")
def like_post(
    current_post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    like_post_or_comment(db=db, current_user=current_user, current_entity=current_post)


@router.delete("/{post_id}/likes")
def dislike_post(
    current_post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    dislike_post_or_comment(
        db=db, current_entity=current_post, current_user=current_user
    )


@router.post("/{post_id}/comments/{comment_id}/likes")
def like_comment(
    current_comment: Comment = Depends(get_current_comment),
    current_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    like_post_or_comment(
        db=db, current_entity=current_comment, current_user=current_user
    )


@router.delete("/{post_id}/comments/{comment_id}/likes")
def dislike_comment(
    current_comment: Comment = Depends(get_current_comment),
    current_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    dislike_post_or_comment(
        db=db, current_entity=current_comment, current_user=current_user
    )
