from .base import BaseModel


class UserResponse(BaseModel):
    username: str
    email: str
    name: str


class UserCreate(BaseModel):
    username: str
    email: str
    name: str
    password: str
