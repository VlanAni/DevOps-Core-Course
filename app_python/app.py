from typing import Any, Literal, get_args, TypeAlias
import platform
import os
import socket
from datetime import datetime, timezone
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic_settings import BaseSettings

NAME = "test"
VERSION = "1.0"
DESCRIPTION = "lab1"
FRAMEWORK = "fast-api"
ENDPOINTS: list[dict[str, str]] = [
    {"path": "/", "method": "GET", "description": "returns information about server"},
    {"path": "/health", "method": "GET", "description": "server state"},
]
START_TIME = datetime.now(timezone.utc)

RootRequirements: TypeAlias = Literal[
    "service", "system", "runtime", "request", "endpoints"
]


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False


class CollectDataException(Exception):
    pass


class FailToExtractSystemData(CollectDataException):
    pass


class FailToExtractRequestData(CollectDataException):
    pass


logging.basicConfig(format="%(levelno)s: %(message)s", level=logging.INFO)

settings = Settings()
app = FastAPI(
    debug=settings.debug,
)


@app.exception_handler(StarletteHTTPException)
async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):

    timestamp = int(datetime.now().timestamp())

    logging.info(f"timestamp: {timestamp}, request: {request}, error: {exc}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "cause": exc.detail,
            "path": request.url.path,
            "method": request.method,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.exception("Unexpected error")

    return JSONResponse(
        status_code=500,
        content={
            "cause": "internal server error",
            "path": request.url.path,
            "method": request.method,
        },
    )


@app.get("/")
def root(request: Request):

    data = _build_root_response(request=request)

    return JSONResponse(content=data, status_code=200)


@app.get("/health")
def health():

    now = datetime.now(timezone.utc)

    data: dict[str, Any] = {
        "status": "OK",
        "timestamp": int(now.timestamp()),
        "uptime_seconds": int((now - START_TIME).total_seconds()),
    }

    return JSONResponse(content=data, status_code=200)


def _build_root_response(request: Request) -> dict[str, Any]:

    data: dict[str, Any] = {}

    for literal in get_args(RootRequirements):

        data[literal] = _root_response_helper(data=literal, request=request)

    return data


def _root_response_helper(
    data: RootRequirements, request: Request
) -> dict[str, Any] | list[Any]:

    match data:

        case "service":

            return get_service_data()

        case "system":

            return get_system_data()

        case "runtime":

            return get_runtime_data()

        case "request":

            return get_request_data(request=request)

        case "endpoints":

            return get_endpoint_data()

        case _:

            raise ValueError(f"unknown root requirement {data}")


def get_service_data() -> dict[str, Any]:
    return {
        "name": NAME,
        "version": VERSION,
        "description": DESCRIPTION,
        "framework": FRAMEWORK,
    }


def get_system_data() -> dict[str, Any]:

    data: dict[str, Any] = {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count(),
        "python_version": platform.python_version(),
    }

    for key, value in data.items():  # type: ignore [value can be String, Int, None]
        if value is None or value == "":
            raise FailToExtractSystemData(f"failed to get {key}")

    return data


def get_runtime_data() -> dict[str, Any]:

    now = datetime.now(timezone.utc)

    uptime_seconds = int((now - START_TIME).total_seconds())

    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return {
        "uptime_seconds": uptime_seconds,
        "uptime_human": f"{hours} hours, {minutes} minutes",
        "current_time": now.isoformat(),
        "timezone": datetime.now().astimezone().tzname(),
    }


def get_request_data(request: Request) -> dict[str, Any]:

    data: dict[str, Any] = {}

    if request.client is None:
        raise FailToExtractRequestData(f"client is None")

    data["client_ip"] = request.client.host
    data["user_agent"] = request.headers.get("user-agent", "")
    data["method"] = request.method
    data["path"] = request.url.path

    return data


def get_endpoint_data() -> list[dict[str, str]]:
    return ENDPOINTS


if __name__ == "__main__":
    uvicorn.run(
        app="app:app", host=settings.host, port=settings.port, reload=settings.debug
    )
