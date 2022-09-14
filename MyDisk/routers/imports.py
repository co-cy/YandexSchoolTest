from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from fastapi import status


from MyDisk.schemas import SystemItemImportRequest
from MyDisk.helper import datetime_is_correct
from MyDisk.database.models.node import Node
from MyDisk.database import get_db


router = APIRouter()


@router.post("/imports")
def imports(body: SystemItemImportRequest, db_session=Depends(get_db)):
    list_update: list[tuple[str, int]] = []

    date = datetime_is_correct(body.updateDate)
    for item in body.items:
        new_node = Node(**item.dict(), date_string=body.updateDate, date=date)

        node: Node = db_session.query(Node).get(item.id)
        if node:
            if node.parentId == item.parentId:
                list_update.append((item.parentId, item.size - node.size))
            else:
                list_update.append((item.parentId, item.size))
                list_update.append((node.parentId, -node.size))
        elif item.parentId:
            list_update.append((item.parentId, item.size))

        db_session.merge(new_node)
    db_session.commit()

    for parent_id, add_size in list_update:
        parent: Node = db_session.query(Node).get(parent_id)
        if parent.parentId:
            list_update.append((parent.parentId, add_size))

        parent.size += add_size
        parent.date_string = body.updateDate
        parent.date = date

        db_session.add(parent)
    db_session.commit()

    return JSONResponse(status_code=200, content={
        "code": status.HTTP_200_OK,
        "message": "Вставка или обновление прошли успешно."
    })
