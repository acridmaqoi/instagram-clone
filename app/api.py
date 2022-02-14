from fastapi import APIRouter

from app.auth.views import router

api = APIRouter()


@api.get("/health")
def get_health():
    return {"status": "ok"}


api.include_router(router)
