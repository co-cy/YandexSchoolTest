from fastapi import FastAPI

from MyDisk.routers import index


def routes_initialization(app: FastAPI) -> None:
    app.include_router(index.router)
