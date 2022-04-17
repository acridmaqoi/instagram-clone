from fastapi import Depends
from fastapi.routing import APIRouter
from instagram.database.core import get_db
from instagram.post.models import CommentCreate, Post
from instagram.post.views import get_current_post
from instagram.user.models import InstagramUser
from instagram.user.service import get_authenticated_user
from sqlalchemy.orm import Session

from .service import create, delete

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/{post_id}")
def create_comment(
    comment_in: CommentCreate,
    current_user: InstagramUser = Depends(get_authenticated_user),
    current_post: Post = Depends(get_current_post),
    db: Session = Depends(get_db),
):
    create(
        db=db,
        comment_in=comment_in,
        post=current_post,
        current_user=current_user,
    )


@router.delete("/{post_id}/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: InstagramUser = Depends(get_authenticated_user),
    current_post: Post = Depends(get_current_post),
    db: Session = Depends(get_db),
):
    delete(db=db, post_id=current_post.id, comment_id=comment_id)
