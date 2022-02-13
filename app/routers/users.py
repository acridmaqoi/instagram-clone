from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..auth import create_user_token, get_current_user
from ..internal.controllers import user_controller
from ..internal.database import get_db
from ..internal.models.user import User
from ..schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db=db, created_user=user)


@router.get("/current", response_model=UserResponse)
def get_current_user(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return user


@router.put("/current", response_model=UserResponse)
def update_current_user(
    updated_user: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return user_controller.update_user(
        db=db, updated_user=updated_user, user_id=user.id
    )


@router.delete("/current")
def delete_current_user(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    user_controller.delete_user(db=db, user_id=user.id)
    return {"ok": True}


@router.post("/session")
async def create_user_session(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    if not user_controller.verify_user_password(
        db=db, username=form_data.username, password=form_data.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_user_token(username=form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}
