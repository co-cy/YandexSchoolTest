from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import status


from MyDisk.schemas import SystemItemImportRequest
from MyDisk.database.models.node import Node
from MyDisk.database import get_db


router = APIRouter()


@router.post("/imports")
def imports(body: SystemItemImportRequest, db_session=Depends(get_db)):
    for item in body.items:
        new_node = Node(**item.dict(), date=body.updateDate)
        db_session.merge(new_node)
    db_session.commit()

    return JSONResponse(status_code=200, content={
        "code": status.HTTP_200_OK,
        "message": "Вставка или обновление прошли успешно."
    })
