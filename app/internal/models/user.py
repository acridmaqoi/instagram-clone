from typing import Any

from passlib.context import CryptContext
from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import Session, relationship

from .record import Record

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Record):
    __tablename__ = "user"

    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)

    posts = relationship("Post", backref="user")
    comments = relationship("Comment", backref="user")
    likes = relationship("Like", back_populates="user", lazy="dynamic")
