from fastapi import FastAPI

from MyDisk.routers import imports


def routes_initialization(app: FastAPI) -> None:
    app.include_router(imports.router)
