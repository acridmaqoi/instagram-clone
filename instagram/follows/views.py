from fastapi import APIRouter, Depends
from instagram.database.core import get_db
from instagram.user.models import InstagramUser
from instagram.user.service import get_authenticated_user, get_current_user
from sqlalchemy.orm import Session

from .service import follow, unfollow

router = APIRouter(prefix="/friendships", tags=["friendships"])


@router.post("/{user_id}/follow")
def follow_user(
    user: InstagramUser = Depends(get_current_user),
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    follow(db=db, user=user, current_user=current_user)


@router.post("/{user_id}/unfollow")
def unfollow_user(
    user: InstagramUser = Depends(get_current_user),
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    unfollow(db=db, user=user, current_user=current_user)
