import typing

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from instagram.auth.views import router as auth_router
from instagram.friendship.views import router as friend_router
from instagram.post.views import router as post_router
from instagram.utils.views import router as util_router


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
api.include_router(util_router)
