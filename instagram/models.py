import datetime
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Optional

from pydantic import BaseModel, root_validator
from sqlalchemy import Column, DateTime, func

user_context = ContextVar("user_ctx")


@contextmanager
def set_user_context(state):
    token = user_context.set(state)
    yield
    user_context.reset(token)


def user_context_response(pydantic_model, model, user):
    with set_user_context(user.id):
        model = pydantic_model.from_orm(model)
        return model


class InstagramBase(BaseModel):
    class Config:
        orm_mode = True


class TimeStampMixin(object):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
