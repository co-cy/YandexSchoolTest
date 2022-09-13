from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.requests import Request
from fastapi import FastAPI, status

from MyDisk.routers import routes_initialization
from MyDisk.config import FastApiConfig

# TODO: Переместить логику в отдельное место
from MyDisk.database.models import node
from MyDisk.database import engine

node.Base.metadata.create_all(bind=engine)

app = FastAPI(**FastApiConfig())
routes_initialization(app)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc) -> Response:
    return JSONResponse(content={
        "code": status.HTTP_400_BAD_REQUEST,
        "message": "Невалидная схема документа или входные данные не верны."
    }, status_code=status.HTTP_400_BAD_REQUEST)
