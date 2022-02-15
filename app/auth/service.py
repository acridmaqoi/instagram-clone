import email
from datetime import datetime, timedelta
from typing import Optional

from app.auth.models import InstagramUser
from app.database.core import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .models import InstagramUser, UserRegister

# TODO make env variables
SECRET_KEY = "c13836d0e76c81a92a65ebb2f00bdb19c058e799c658559a6a73918e689bc99e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
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
    user = get_user_by_email(db=db, email=email)
    if user is None:
        raise credentials_exception
    return user


def get_user(db: Session, user_id: int) -> Optional[InstagramUser]:
    return db.query(InstagramUser).filter(InstagramUser.id == user_id).one_or_none()


def get_user_by_email(db: Session, email: str) -> Optional[InstagramUser]:
    return db.query(InstagramUser).filter(InstagramUser.email == email).one_or_none()


def create_user(db: Session, user_in: UserRegister):
    password = bytes(user_in.password, "utf-8")

    user = InstagramUser(**user_in.dict(exclude={"password"}), password=password)
    db.add(user)
    db.commit()
    return user
