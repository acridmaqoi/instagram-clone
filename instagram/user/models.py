from datetime import datetime, timedelta
from enum import unique
from typing import Optional

import bcrypt
from instagram.database.core import Base
from instagram.models import InstagramBase
from jose import jwt
from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy import Column, Integer, LargeBinary, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

SECRET_KEY = "c13836d0e76c81a92a65ebb2f00bdb19c058e799c658559a6a73918e689bc99e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 60


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class InstagramUser(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(LargeBinary, nullable=False)
    name = Column(String)

    posts = relationship("Post")
    likes = relationship("Like", back_populates="user")
    followers = relationship("Follow", foreign_keys="[Follow.to_user_id]")
    following = relationship("Follow", foreign_keys="[Follow.from_user_id]")

    @hybrid_property
    def post_count(self):
        return len(self.posts)

    @hybrid_property
    def follower_count(self):
        return len(self.followers)

    @hybrid_property
    def follow_count(self):
        return len(self.following)

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)).timestamp()
        data = {
            "exp": exp,
            "email": self.email,
        }
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


class UserBase(InstagramBase):
    username: str
    email: EmailStr
    name: Optional[str]


class UserRead(UserBase):
    id: int
    post_count: int
    follower_count: int
    follow_count: int


class UserLogin(UserBase):
    password: str


class UserRegister(UserBase):
    password: str

    @validator("password", pre=True, always=True)
    def hash_password(cls, password):
        return hash_password(password)


class UserLoginResponse(InstagramBase):
    token: Optional[str] = Field(None, nullable=False)


class UserRegisterResponse(InstagramBase):
    token: Optional[str] = Field(None, nullable=False)
