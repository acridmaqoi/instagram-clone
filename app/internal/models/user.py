import bcrypt
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from .record import Record, RecordNotFound


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
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(8))

        return super().create(db=db, hashed_password=hashed_password, **data)

    @classmethod
    def update_by_id(cls, db: Session, id: int, password: str, **data):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(8))

        return super().update_by_id(
            db=db, id=id, hashed_password=hashed_password, **data
        )
