from pydantic import BaseModel


class InstagramBase(BaseModel):
    class Config:
        orm_mode = True
