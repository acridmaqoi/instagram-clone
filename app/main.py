from fastapi import FastAPI

from .internal.database import Base, engine
from .routers import posts

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/hello")
def hello_world():
    return {"message": "Hello, World!"}


app.include_router(posts.router, prefix="/posts", tags=["posts"])
