import email
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from instagram.database.core import get_db
from instagram.follow.models import Follow
from instagram.user.models import InstagramUser
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .models import InstagramUser, UserRegister, UserUpdate

# TODO make env variables
SECRET_KEY = "c13836d0e76c81a92a65ebb2f00bdb19c058e799c658559a6a73918e689bc99e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_authenticated_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> InstagramUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_by_email(db=db, email=email)
    if user is None:
        raise credentials_exception
    return user


def get_current_user(
    user_id: int, db: Session = Depends(get_db)
) -> Optional[InstagramUser]:
    user = get(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found",
        )

    return user


def add_user_meta(
    db: Session, user: InstagramUser, viewing_user: InstagramUser | None = None
) -> None:
    if viewing_user is None:
        return

    if user.id == viewing_user.id:
        return

    user.followed_by_viewer = user.id in viewing_user.following_ids
    user.follows_viewer = user.id in viewing_user.followers_ids

    mutual_followers_qry = (
        db.query(InstagramUser)
        .filter(InstagramUser.id.in_(viewing_user.following_ids))
        .filter(InstagramUser.id.in_(user.following_ids))
    )

    user.mutual_followers["usernames"] = [
        user.username for user in mutual_followers_qry.limit(3).all()
    ]
    user.mutual_followers["count"] = mutual_followers_qry.count()


def get(
    db: Session, user_id: int, viewing_user: InstagramUser | None = None
) -> Optional[InstagramUser]:
    user = db.query(InstagramUser).filter(InstagramUser.id == user_id).one_or_none()
    return user


def get_by_username(
    db: Session, username: str, viewing_user: InstagramUser | None = None
) -> Optional[InstagramUser]:
    user = (
        db.query(InstagramUser).filter(InstagramUser.username == username).one_or_none()
    )
    return user


def get_by_email(db: Session, email: str) -> Optional[InstagramUser]:
    user = db.query(InstagramUser).filter(InstagramUser.email == email).one_or_none()
    return user


def create(db: Session, user_in: UserRegister):
    password = bytes(user_in.password, "utf-8")

    user = InstagramUser(**user_in.dict(exclude={"password"}), password=password)
    db.add(user)
    db.commit()
    return user


def update(db: Session, user_in: UserUpdate, current_user: InstagramUser):
    for k, v in user_in.dict(exclude_unset=True).items():
        setattr(current_user, k, v)
        db.commit()
    return current_user
