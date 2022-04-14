from instagram.user.models import InstagramUser
from psycopg2.errors import CheckViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import Follow


def create(db: Session, from_user: InstagramUser, to_user: InstagramUser) -> None:
    try:
        db.add(Follow(from_user_id=from_user.id, to_user_id=to_user.id))
        db.commit()
    except IntegrityError as e:
        if isinstance(e.orig, CheckViolation):
            db.rollback()
            print(f"user {from_user} cannot follow themselves")
        if isinstance(e.orig, UniqueViolation):
            db.rollback()
            print(f"user {from_user} has already followed {to_user}")
        else:
            raise


def delete(db: Session, from_user: InstagramUser, to_user: InstagramUser) -> None:
    follow = (
        db.query(Follow)
        .filter(Follow.from_user_id == from_user.id)
        .filter(Follow.to_user_id == to_user.id)
        .one_or_none()
    )

    if follow:
        db.delete(follow)
        db.commit()
    else:
        print(f"user {from_user} is not following {to_user}")
