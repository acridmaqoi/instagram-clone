from ast import For
from datetime import datetime, timedelta
from enum import unique
from types import SimpleNamespace
from typing import ForwardRef, List, Optional

import bcrypt
from instagram.database.core import Base
from instagram.follows.models import Follow
from instagram.models import InstagramBase
from jose import jwt
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
from sqlalchemy import Column, Integer, LargeBinary, String, orm, select
from sqlalchemy.ext.associationproxy import association_proxy
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
    picture_url = Column(String)

    posts = relationship("Post")
    saved_posts = relationship("Save")
    likes = relationship("Like", back_populates="user")
    followers_follows = relationship("Follow", foreign_keys="[Follow.to_user_id]")
    following_follows = relationship("Follow", foreign_keys="[Follow.from_user_id]")

    followers = association_proxy("followers_follows", "from_user")
    following = association_proxy("following_follows", "to_user")
    followers_ids = association_proxy("followers_follows", "from_user_id")
    following_ids = association_proxy("following_follows", "to_user_id")

    @hybrid_property
    def post_count(self):
        return len(self.posts)

    @hybrid_property
    def follower_count(self):
        return len(self.followers_follows)

    @hybrid_property
    def following_count(self):
        return len(self.following_follows)

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

    @orm.reconstructor
    def init_on_load(self):
        self.mutual_followers = {"count": 0, "usernames": []}
        self.followed_by_viewer = False
        self.follows_viewer = False


class UserBase(InstagramBase):
    username: str
    email: EmailStr
    name: Optional[str]
    picture_url: Optional[HttpUrl]


class UserMutualRead(InstagramBase):
    usernames: List[str]
    count: int


class UserReadSimple(UserBase):
    id: int
    post_count: int
    follower_count: int
    following_count: int


class UserReadFull(UserReadSimple):
    mutual_followers: UserMutualRead
    followed_by_viewer: bool
    follows_viewer: bool


class UserReadSimpleList(InstagramBase):
    users: List[UserReadSimple]
    count: int


class UserReadFullList(InstagramBase):
    users: List[UserReadFull]
    count: int


class UserUpdate(InstagramBase):
    name: Optional[str]
    picture_url: Optional[HttpUrl]


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
