from fastapi import APIRouter, Depends

from MyDisk.database.models.node import Node
from MyDisk.database import get_db


router = APIRouter()


@router.get("/nodes/{node_id}")
def get_nodes(node_id: str, db_session=Depends(get_db)):
    node = db_session.query(Node).get(node_id)

    return node.json()
