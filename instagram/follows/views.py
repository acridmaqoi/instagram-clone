from fastapi import APIRouter, Depends
from instagram.database.core import get_db
from instagram.user.models import InstagramUser
from instagram.user.service import get_authenticated_user, get_current_user
from sqlalchemy.orm import Session

from .service import create, delete

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
