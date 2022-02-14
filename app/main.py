from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .internal.controllers.record_crud import (
    RecordAlreadyExists,
    RecordNotFound,
    RecordRelationNotFound,
)
from .internal.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(RecordNotFound)
def not_found_exception_handler(request: Request, exc: RecordNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.detail}
    )


@app.exception_handler(RecordAlreadyExists)
@app.exception_handler(RecordRelationNotFound)
def relation_not_found_exception_handler(request: Request, exc: RecordRelationNotFound):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.detail}
    )


@app.get("/hello")
def hello_world():
    return {"message": "Hello, World!"}
