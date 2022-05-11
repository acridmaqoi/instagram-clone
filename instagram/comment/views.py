from asyncio import start_unix_server
from email.policy import HTTP

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from instagram.comment.models import Comment
from instagram.database.core import get_db
from instagram.models import user_context_response
from instagram.post.models import CommentCreate, Post
from instagram.post.views import get_current_post
from instagram.user.models import InstagramUser
from instagram.user.service import get_authenticated_user
from sqlalchemy.orm import Session

from .models import CommentRead
from .service import create, delete, get

router = APIRouter(prefix="/comments", tags=["comments"])


def get_current_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    comment = get(db=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id={comment_id} not found",
        )
    return comment


@router.post("/{post_id}")
def create_comment(
    comment_in: CommentCreate,
    current_user: InstagramUser = Depends(get_authenticated_user),
    current_post: Post = Depends(get_current_post),
    db: Session = Depends(get_db),
):
    comment = create(
        db=db,
        comment_in=comment_in,
        post=current_post,
        current_user=current_user,
    )

    return user_context_response(CommentRead, comment, current_user)


@router.delete("/{comment_id}")
def delete_comment(
    comment: Comment = Depends(get_current_comment),
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    if current_user.id != comment.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    delete(db=db, comment_id=comment.id)
