from app.auth.models import InstagramUser
from app.auth.service import get_current_user
from app.database.core import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .models import Post, PostCreate, PostDelete, PostRead
from .service import create, delete, get

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


@router.delete("/{post_id}", response_model=PostDelete)
def delete_post(
    post: Post = Depends(get_current_post),
    user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete(db=db, post_id=post.id)
