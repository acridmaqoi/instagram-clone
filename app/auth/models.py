from datetime import datetime, timedelta
from enum import unique
from typing import Optional

import bcrypt
from app.database.core import Base
from app.models import InstagramBase
from jose import jwt
from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy import Column, Integer, LargeBinary, String

SECRET_KEY = "c13836d0e76c81a92a65ebb2f00bdb19c058e799c658559a6a73918e689bc99e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class InstagramUser(Base):
    # __table_args__ = {"schema": "instagram_core"}

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(LargeBinary, nullable=False)

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
        data = {
            "exp": exp,
            "email": self.email,
        }
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


class UserBase(InstagramBase):
    username: str
    email: EmailStr


class UserRead(UserBase):
    id: int


class UserLogin(UserBase):
    password: str


class UserRegister(UserBase):
    password: str

    @validator("password", pre=True, always=True)
    def password_required(cls, password):
        return hash_password(password)


class UserLoginResponse(InstagramBase):
    token: Optional[str] = Field(None, nullable=False)


class UserRegisterResponse(InstagramBase):
    token: Optional[str] = Field(None, nullable=False)
