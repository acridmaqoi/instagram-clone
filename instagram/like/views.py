from profile.models import InstagramUser
from profile.service import get_current_user

from database.core import get_db
from fastapi import APIRouter, Depends
from instagram.post.views import get_current_post
from post.models import Comment, Post, PostCreate, PostRead
from sqlalchemy.orm import Session

from .service import create, delete

router = APIRouter(prefix="/likes", tags=["likes"])


@router.post("/{post_id}")
def create_like(
    current_post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    create(db=db, current_user=current_user, current_post=current_post)


@router.delete("/{post_id}")
def delete_like(
    current_post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete(db=db, current_user=current_user, current_post=current_post)
