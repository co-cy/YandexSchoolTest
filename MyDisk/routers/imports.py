from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from fastapi import status

from MyDisk.schemas import SystemItemImportRequest, SystemItemType
from MyDisk.helper import str_to_datetime
from MyDisk.database.models.node import Node
from MyDisk.database import get_db

router = APIRouter()


@router.post("/imports")
def imports(body: SystemItemImportRequest, db_session=Depends(get_db)):
    date = str_to_datetime(body.updateDate)

    dict_old: dict[str, Node] = {item.id: item for item in body.items}
    dict_result: dict[str, Node] = {}

    for node_id in dict_old.keys():
        dict_result[node_id] = db_session.query(Node).get(node_id)

    parent_update_list: list[tuple[str, int]] = []
    for node_id in dict_old.keys():
        node = dict_result.get(node_id)
        if node:
            old_node = dict_old.get(node_id)
            old_node_parent_id = old_node.parentId
            node_parent_id = node and node.parentId

            if old_node_parent_id and node_parent_id and old_node_parent_id == node_parent_id:
                if node.type != SystemItemType.folder:
                    added_size = node.size - old_node.size
                    if added_size:
                        parent_update_list.append((node_parent_id, added_size))
                    continue
            else:
                if node_parent_id:
                    parent_update_list.append((node_parent_id, node.size))

                if old_node_parent_id:
                    parent_update_list.append((old_node_parent_id, -node.size))
            node.update(dict_old.get(node_id).dict(), body.updateDate)
        else:
            dict_result[node_id] = Node(**dict_old[node_id].dict(), date_string=body.updateDate, date=date)
            if dict_result[node_id].parentId:
                parent_update_list.append((dict_result[node_id].parentId, dict_result[node_id].size))

    for parent_id, add_size in parent_update_list:
        parent: Node = dict_result.get(parent_id)
        if not parent:
            parent = db_session.query(Node).get(parent_id)
            dict_result[parent_id] = parent

        parent.size += add_size
        parent.date_string = body.updateDate

        parent.date = date
        if parent.parentId:
            parent_update_list.append((parent.parentId, add_size))

    for node in dict_result.values():
        db_session.add(node)
    db_session.commit()

    return JSONResponse(status_code=200, content={
        "code": status.HTTP_200_OK,
        "message": "Вставка или обновление прошли успешно."
    })
