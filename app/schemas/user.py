from pydantic import BaseModel


class UserResponse(BaseModel):
    username: str
    email: str
    name: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    name: str
    password: str
