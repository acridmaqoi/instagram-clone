from http.client import HTTPException

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..internal.database import get_db
from .models import (
    InstagramUser,
    UserLogin,
    UserLoginResponse,
    UserRead,
    UserRegister,
    UserRegisterResponse,
)
from .service import create_user, get_current_user, get_user, get_user_by_email

router = APIRouter(prefix="/auth")


@router.get("/current", response_model=UserRead)
def get_logged_in_user(
    current_user: InstagramUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return current_user


@router.post("/login", response_model=UserLoginResponse)
def login_user(user_in: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=user_in.email)
    if user and user.check_password(user_in.password):
        return user


@router.post("/register", response_model=UserRegisterResponse)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)

    return create_user(db=db, user_in=user_in)
