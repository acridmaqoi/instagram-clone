from datetime import datetime, timedelta
from enum import unique
from typing import List, Optional

import bcrypt
from instagram.database.core import Base, SessionLocal
from instagram.follow.models import Follow
from instagram.models import InstagramBase, user_context
from jose import jwt
from pydantic import BaseModel, EmailStr, Field, HttpUrl, root_validator, validator
from sqlalchemy import Column, Integer, LargeBinary, String, orm, select
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import and_, true

db = SessionLocal()

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

    liked_entities = association_proxy("likes", "entity")
    liked_entities_ids = association_proxy("likes", "entity_id")
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

    @hybrid_method
    def is_following(self, user: "InstagramUser"):
        return any(user.id in self.following_ids)

    @is_following.expression
    def is_following(cls, user):
        return and_(true(), cls.following.any(user_id=user.id))

    @hybrid_method
    def is_followed_by(self, user: "InstagramUser"):
        return any(user.id in self.followers_ids)

    @is_followed_by.expression
    def is_followed_by(cls, user):
        return and_(true(), cls.followers.any(user_id=user.id))

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

    @root_validator
    def follows_viewer(cls, values):
        try:
            if user_context.get():
                values["follows_viewer"] = (
                    db.query(InstagramUser.is_following(user_context.get()))
                    .filter(InstagramUser.id == values["id"])
                    .scalar()
                )
        except:
            pass
        return values

    @root_validator
    def followed_by_viewer(cls, values):
        try:
            if user_context.get():
                values["followed_by_viewer"] = (
                    db.query(InstagramUser.is_followed_by(user_context.get()))
                    .filter(InstagramUser.id == values["id"])
                    .scalar()
                )
        except:
            pass
        return values


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
