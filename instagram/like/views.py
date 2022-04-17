from fastapi import APIRouter, Depends
from instagram.database.core import get_db
from instagram.post.models import Post, PostCreate, PostRead
from instagram.post.views import get_current_post
from instagram.user.models import InstagramUser
from instagram.user.service import get_authenticated_user
from sqlalchemy.orm import Session

from .service import create, delete

router = APIRouter(prefix="/likes", tags=["likes"])


@router.post("/{post_id}")
def create_like(
    current_post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    create(db=db, current_user=current_user, current_post=current_post)


@router.delete("/{post_id}")
def delete_like(
    current_post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    delete(db=db, current_user=current_user, current_post=current_post)
