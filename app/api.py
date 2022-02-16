import typing

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.auth.views import router as auth_router
from app.friendship.views import router as friend_router
from app.post.views import router as post_router


class ApiResponse(BaseModel):
    status: str


api = APIRouter()


@api.get("/health")
def get_health():
    raise HTTPException(404)
    return {"status": "ok"}


api.include_router(auth_router)
api.include_router(post_router)
api.include_router(friend_router)
