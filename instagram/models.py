import datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, func


class InstagramBase(BaseModel):
    class Config:
        orm_mode = True


class TimeStampMixin(object):
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
