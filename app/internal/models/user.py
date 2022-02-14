from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import Session, relationship


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "c13836d0e76c81a92a65ebb2f00bdb19c058e799c658559a6a73918e689bc99e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480


# class User(Record):
#    __tablename__ = "user"
#
#    username = Column(String, nullable=False, unique=True)
#    hashed_password = Column(String, nullable=False)
#    email = Column(String, nullable=False, unique=True)
#    name = Column(String, nullable=False)
#
#    posts = relationship("Post", backref="user")
#    comments = relationship("Comment", backref="user")
#    likes = relationship("Like", back_populates="user", lazy="dynamic")
