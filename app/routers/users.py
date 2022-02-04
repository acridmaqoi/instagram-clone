from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..internal.database import get_db
from ..internal.models.user import User
from ..schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return User.create(db=db, **user.dict())


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return User.get_by_id(db=db, id=user_id)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    User.delete_by_id(db=db, id=user_id)
    return {"ok": True}
