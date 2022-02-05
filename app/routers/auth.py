from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..auth import create_user_token, get_current_user
from ..internal.database import get_db
from ..internal.models.user import User
from ..schemas.user import UserResponse

router = APIRouter()


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
