from fastapi import APIRouter, Depends, HTTPException, status
from instagram.database.core import get_db
from instagram.like.models import LikeableEntity
from instagram.post.models import Post, PostCreate, PostRead
from instagram.post.views import get_current_post
from instagram.user.models import InstagramUser, UserReadFullList, UserReadSimpleList
from instagram.user.service import get_authenticated_user
from sqlalchemy.orm import Session

from .service import create, delete, get_all, get_likeable

router = APIRouter(prefix="/likes", tags=["likes"])


def get_current_likeable(likeable_id: int, db: Session = Depends(get_db)):
    likeable = get_likeable(db=db, likeable_id=likeable_id)
    if not likeable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Likeable with id={likeable_id} not found",
        )
    return likeable


@router.post("/{likeable_id}")
def create_like(
    likeable: LikeableEntity = Depends(get_current_likeable),
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    create(db=db, current_user=current_user, likeable=likeable)


@router.get("", response_model=UserReadFullList)
def get_likes(
    likeable: LikeableEntity = Depends(get_current_likeable),
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    likes = get_all(db=db, likeable_id=likeable.id)
    return {"users": [like.user for like in likes], "count": len(likes)}


@router.delete("/{likeable_id}")
def delete_like(
    likeable: Post = Depends(get_current_likeable),
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    delete(db=db, likeable=likeable, current_user=current_user)
