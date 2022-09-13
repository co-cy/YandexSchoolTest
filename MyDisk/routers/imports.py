from datetime import datetime
from fastapi import APIRouter, Depends

from MyDisk.schemas import SystemItemImportRequest
from MyDisk.database.models.node import Node
from MyDisk.database import get_db


router = APIRouter()


@router.post("/imports")
def imports(body: SystemItemImportRequest, db_session=Depends(get_db)):
    date = datetime.strptime(body.updateDate, "%Y-%m-%dT%H:%M:%S.%fZ")

    for item in body.items:
        new_node = Node(**item.dict(), date=date)
        db_session.merge(new_node)
    db_session.commit()

    return "OK"
