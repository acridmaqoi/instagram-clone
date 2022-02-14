from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api import api as api_router

from .internal.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
api = FastAPI()


api.include_router(api_router)

app.mount("/api/", app=api)
