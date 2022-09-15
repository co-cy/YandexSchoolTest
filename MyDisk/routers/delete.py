from fastapi.exceptions import RequestValidationError
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from MyDisk.helper import str_to_datetime
from MyDisk.database.models.node import Node
from MyDisk.database import get_db

router = APIRouter()


@router.delete("/delete/{node_id}")
def delete(node_id: str, date: str, db_session=Depends(get_db)):

    date_datetime = str_to_datetime(date)
    if not date_datetime:
        raise RequestValidationError("Bad date_string")

    node = db_session.query(Node).get(node_id)
    if not node:
        return JSONResponse(status_code=404, content={
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Item not found"
        })

    if node.parentId:
        list_parent = [node.parentId]
        for parent_id in list_parent:
            parent: Node = db_session.query(Node).get(parent_id)
            if parent.parentId:
                list_parent.append(parent.parentId)

            parent.size -= node.size
            parent.date_string = date
            parent.date = date_datetime

            db_session.add(parent)
    db_session.delete(node)
    db_session.commit()

    return JSONResponse(status_code=200, content={
        "code": status.HTTP_200_OK,
        "message": "Удаление прошло успешно."
    })
