import typing

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException

from instagram.api import api as api_router


class BaseJSONResponse(JSONResponse):
    def render(self, content: typing.Any) -> bytes:
        if content:
            content["status"] = "ok"
        else:
            content = {"status": "ok"}
        return super().render(content)


app = FastAPI()

api = FastAPI(default_response_class=BaseJSONResponse)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.exception_handler(HTTPException)
async def exception_handler(request, exc):
    return JSONResponse(
        {"detail": exc.detail, "status": "fail"}, status_code=exc.status_code
    )


api.include_router(api_router)

app.mount("/api/", app=api)
