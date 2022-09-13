from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from MyDisk.database.models.node import Node
from MyDisk.database import get_db


router = APIRouter()


@router.get("/nodes/{node_id}")
def get_nodes(node_id: str, db_session=Depends(get_db)):
    node = db_session.query(Node).get(node_id)
    if not node:
        return JSONResponse(status_code=404, content={
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Item not found"
        })

    return node.json()
