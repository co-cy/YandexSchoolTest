from fastapi import FastAPI

from MyDisk.routers import routes_initialization
from MyDisk.config import FastApiConfig

# TODO: Переместить логику в отдельное место
from MyDisk.database.models import node
from MyDisk.database import engine

node.Base.metadata.create_all(bind=engine)

app = FastAPI(**FastApiConfig())
routes_initialization(app)
