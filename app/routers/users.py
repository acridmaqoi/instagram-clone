from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..auth import create_user_token, get_current_user
from ..internal.database import get_db
from ..internal.models.user import User
from ..schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return User.create(db=db, **user.dict())


@router.get("/current", response_model=UserResponse)
def get_current_user(
    user: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    User.delete_by_id(db=db, id=user_id)
    return {"ok": True}


@router.post("/session")
async def create_user_session(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    if not User.verify_password(
        db=db, username=form_data.username, password=form_data.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_user_token(username=form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}
