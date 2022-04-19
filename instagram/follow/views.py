from fastapi import APIRouter, Depends
from instagram.database.core import get_db
from instagram.user.models import InstagramUser, UserReadSimple, UserReadSimpleList
from instagram.user.service import get_authenticated_user, get_current_user
from sqlalchemy.orm import Session

from .service import create, delete, get_all_followers, get_all_following

router = APIRouter(prefix="/follows", tags=["follows"])


@router.post("/{user_id}")
def create_follow(
    from_user: InstagramUser = Depends(get_authenticated_user),
    to_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    create(db=db, from_user=from_user, to_user=to_user)


@router.delete("/{user_id}")
def delete_follow(
    from_user: InstagramUser = Depends(get_authenticated_user),
    to_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete(db=db, from_user=from_user, to_user=to_user)


@router.get("/{user_id}/following", response_model=UserReadSimpleList)
def get_following(
    user: InstagramUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    return {"users": list(user.following), "count": len(user.following)}


@router.get("/{user_id}/followers", response_model=UserReadSimpleList)
def get_followers(user: InstagramUser = Depends(get_current_user)):
    return {"users": list(user.followers), "count": len(user.followers)}
