from fastapi import Depends
from fastapi.routing import APIRouter
from instagram.database.core import get_db
from instagram.post.models import Post, PostReadList
from instagram.post.views import get_current_post
from instagram.user.models import InstagramUser
from instagram.user.service import get_authenticated_user
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .service import create, delete, get_all_posts

router = APIRouter(prefix="/saves", tags=["save"])


@router.post("/{post_id}")
def create_save(
    post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    create(db=db, post=post, current_user=current_user)


@router.get("", response_model=PostReadList)
def get_saved(
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    posts = get_all_posts(db=db, user=current_user)
    return {"posts": posts, "count": len(posts)}


@router.delete("/{post_id}")
def delete_save(
    post: Post = Depends(get_current_post),
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    delete(db=db, post=post, current_user=current_user)
