from fastapi import APIRouter, Depends

from MyDisk.database.models.node import Node
from MyDisk.database import get_db


router = APIRouter()


@router.delete("/delete/{node_id}")
def delete(node_id: str, db_session=Depends(get_db)):
    db_session.delete(db_session.query(Node).filter(Node.id == node_id).one())
    db_session.commit()

    return "OK"
