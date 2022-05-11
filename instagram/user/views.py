from fastapi import APIRouter, Depends, HTTPException, status
from instagram.database.core import get_db
from instagram.models import user_context_response
from sqlalchemy.orm import Session

from .models import (
    InstagramUser,
    UserLogin,
    UserLoginResponse,
    UserReadFull,
    UserReadSimple,
    UserRegister,
    UserRegisterResponse,
    UserUpdate,
)
from .service import (
    create,
    get,
    get_authenticated_user,
    get_by_email,
    get_by_username,
    update,
)

router = APIRouter(prefix="/users", tags=["users"])


def get_current_user(user_id: int, db: Session = Depends(get_db)):
    user = get(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found",
        )
    return user


@router.get("/current", response_model=UserReadFull)
def get_current_in_user(
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    return current_user


@router.patch("/current", response_model=UserReadFull)
def update_current_user(
    user_in: UserUpdate,
    current_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    return update(db=db, user_in=user_in, current_user=current_user)


@router.get("/{user_id}")
def get_user(
    user_id: int,
    viewing_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    user = get(db=db, user_id=user_id, viewing_user=viewing_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The user with this id does not exist."}],
        )

    return user_context_response(UserReadFull, user, viewing_user)


@router.get("/username/{username}", response_model=UserReadFull)
def get_user_by_username(
    username: str,
    viewing_user: InstagramUser = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    user = get_by_username(db=db, username=username, viewing_user=viewing_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The user with this username does not exist."}],
        )

    return user


@router.post("/login", response_model=UserLoginResponse)
def login_user(user_in: UserLogin, db: Session = Depends(get_db)):
    user = get_by_email(db=db, email=user_in.email)
    if user and user.check_password(user_in.password):
        return user

    raise HTTPException(status.HTTP_401_UNAUTHORIZED)


@router.post("/register", response_model=UserRegisterResponse)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    user = get_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)

    return create(db=db, user_in=user_in)
