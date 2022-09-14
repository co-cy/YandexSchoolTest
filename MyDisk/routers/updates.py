from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from datetime import timedelta

from MyDisk.helper import datetime_is_correct
from MyDisk.database.models.node import Node
from MyDisk.database import get_db

router = APIRouter()


@router.get("/updates")
def updates(date: str, db_session=Depends(get_db)):
    datetime = datetime_is_correct(date)
    if not datetime:
        raise RequestValidationError("Bad date_string")

    nodes: list[Node | dict] = db_session.query(Node).filter(Node.type == "FILE",
                                                             Node.date >= datetime - timedelta(days=1),
                                                             Node.date <= datetime).all()

    for i in range(len(nodes)):
        nodes[i] = nodes[i].json()

    return JSONResponse(status_code=200, content={
        "items": nodes
    })
