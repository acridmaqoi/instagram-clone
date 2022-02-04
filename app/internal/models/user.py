from passlib.context import CryptContext
from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from .record import Record, RecordNotFound

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Record):
    __tablename__ = "users"

    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)

    @classmethod
    def get_by_username(cls, db: Session, username: str):
        user = db.query(cls).filter(cls.username == username).one_or_none()
        if not user:
            raise RecordNotFound(record=cls, id=username)
        return user

    @classmethod
    def create(cls, db: Session, password: str, **data):
        hashed_password = pwd_context.hash(password)

        return super().create(db=db, hashed_password=hashed_password, **data)

    @classmethod
    def update_by_id(cls, db: Session, id: int, password: str, **data):
        hashed_password = pwd_context.hash(password)

        return super().update_by_id(
            db=db, id=id, hashed_password=hashed_password, **data
        )

    @classmethod
    def verify_password(cls, db: Session, username: str, password: str):
        user = cls.get_by_username(db=db, username=username)
        return pwd_context.verify(password, user.hashed_password)
