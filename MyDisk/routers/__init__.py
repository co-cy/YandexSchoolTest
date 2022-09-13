from fastapi import FastAPI

from MyDisk.routers import imports, delete


def routes_initialization(app: FastAPI) -> None:
    app.include_router(imports.router)
    app.include_router(delete.router)
