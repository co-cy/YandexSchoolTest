from fastapi.exceptions import RequestValidationError
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime

from MyDisk.database.models.node import Node
from MyDisk.database import get_db


router = APIRouter()


@router.delete("/delete/{node_id}")
def delete(node_id: str, date: str, db_session=Depends(get_db)):

    try:
        datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        raise RequestValidationError("Bad date")

    node = db_session.query(Node).get(node_id)
    if not node:
        return JSONResponse(status_code=404, content={
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Item not found"
        })

    db_session.delete(node)
    db_session.commit()

    return JSONResponse(status_code=200, content={
        "code": status.HTTP_200_OK,
        "message": "Удаление прошло успешно."
    })
