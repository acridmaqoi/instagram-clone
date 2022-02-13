from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..models.user import User
from . import record_crud
from .record_crud import RecordNotFound

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(db: Session, user_id: int):
    return record_crud.get_record_by_id(db=db, id=user_id, model=User)


def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).one_or_none()
    if not user:
        raise RecordNotFound(record=User, col="username", val=username)
    return user


def create_user(db: Session, created_user: UserCreate):
    hashed_password = pwd_context.hash(created_user.password)

    user = User(
        username=created_user.username,
        email=created_user.email,
        name=created_user.name,
        hashed_password=hashed_password,
    )

    return record_crud.write_record(db=db, record=user)


def update_user(db: Session, updated_user: UserUpdate, user_id: int):
    user = record_crud.get_record_by_id(db=db, id=user_id, model=User)

    updated_hashed_password = pwd_context.hash(updated_user.password)

    user.hashed_password = updated_hashed_password
    user.email = updated_user.email
    user.password = updated_user.password

    return record_crud.write_record(db=db, record=user)


def delete_user(db: Session, user_id: int):
    return record_crud.delete_record_by_id(db=db, id=user_id, model=User)


def verify_user_password(db: Session, username: str, password: str):
    user = get_user_by_username(db=db, username=username)
    return pwd_context.verify(password, user.hashed_password)
