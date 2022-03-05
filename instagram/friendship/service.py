from instagram.auth.models import InstagramUser
from sqlalchemy.orm import Session

from .models import Follow


def follow(db: Session, user: InstagramUser, current_user: InstagramUser) -> None:
    if user.id == current_user.id:
        # user cannot follow themselves
        return

    # user can only follow once
    if (
        not db.query(Follow)
        .filter(Follow.from_user_id == current_user.id)
        .filter(Follow.to_user_id == user.id)
        .one_or_none()
    ):
        follow = Follow(from_user_id=current_user.id, to_user_id=user.id)
        db.add(follow)
        db.commit()


def unfollow(db: Session, user: InstagramUser, current_user: InstagramUser) -> None:
    follow = (
        db.query(Follow)
        .filter(Follow.from_user_id == current_user.id)
        .filter(Follow.to_user_id == user.id)
        .one_or_none()
    )

    if follow:
        db.delete(follow)
        db.commit()
