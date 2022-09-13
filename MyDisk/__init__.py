from fastapi import FastAPI

from MyDisk.routers import routes_initialization
from MyDisk.config import FastApiConfig

app = FastAPI(**FastApiConfig())
routes_initialization(app)
