from fastapi import APIRouter, Depends, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from MyDisk.database import get_db
from MyDisk.database.models.node import Node
from MyDisk.helper import datetime_is_correct

router = APIRouter()


@router.delete("/delete/{node_id}")
def delete(node_id: str, date: str, db_session=Depends(get_db)):
    # TODO: При удалении надо вызывть рекурсивное обновление всех родителей и обновлять их вес и дату
    if not datetime_is_correct(date):
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
