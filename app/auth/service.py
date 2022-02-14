import email
from typing import Optional

from app.auth.models import InstagramUser
from sqlalchemy.orm import Session

from .models import InstagramUser, UserRegister


def get_user(db: Session, user_id: int) -> Optional[InstagramUser]:
    return db.query(InstagramUser).filter(InstagramUser.id == user_id).one_or_none()


def get_user_by_email(db: Session, email: str) -> Optional[InstagramUser]:
    return db.query(InstagramUser).filter(InstagramUser.email == email).one_or_none()


def create_user(db: Session, user_in: UserRegister):
    password = bytes(user_in.password, "utf-8")

    user = InstagramUser(**user_in.dict())
    db.add(user)
    db.commit()
    return user
