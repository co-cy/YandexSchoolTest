from pydantic import BaseModel, validator, root_validator

from MyDisk.schemas.item_type import SystemItemType
from MyDisk.helper import str_to_datetime
from MyDisk.database.models.node import Node
from MyDisk.database import get_db
from datetime import datetime


class SystemItem(BaseModel):
    id: str
    url: str | None
    parentId: str | None
    size: int | None
    type: SystemItemType

    @validator("id")
    def validate_id(cls, var: str):
        if 1 > len(var) > 255:
            raise ValueError("Id length does not fit the criteria (0 > Len(id) and Len(id) <= 255)")
        return var

    @root_validator  # validate for url
    def validate_url(cls, values):
        item_type: SystemItemType = values["type"]
        var: str | None = values.get("url")

        if item_type == SystemItemType.folder:
            if var:
                raise ValueError("The folder should not have a url")
        elif item_type == SystemItemType.file:
            if var and len(var) > 255:
                raise ValueError("The url field size must always be less than or equal to 255")

        return values

    @root_validator  # validate for size
    def validate_size(cls, values):
        var: int | None = values.get("size")
        item_type: SystemItemType = values["type"]

        if item_type == SystemItemType.folder:
            if var is not None:
                raise ValueError("The size field should always be null when importing a folder")
            values["size"] = 0
        elif item_type == SystemItemType.file:
            if var <= 0:
                raise ValueError("The size field for files must always be greater than 0")

        return values


class SystemItemImport(SystemItem):
    pass


class SystemItemImportRequest(BaseModel):
    items: list[SystemItemImport]
    updateDate: str

    @validator("items")
    def validate_items(cls, var: list[SystemItemImport]):
        dict_id: dict[str, SystemItemType] = {}

        # Checking for duplicate ID
        for item in var:
            if dict_id.get(item.id):
                raise ValueError("The id of each element is unique among the other elements")
            else:
                dict_id[item.id] = item.type

        for item in var:
            if item.parentId:
                if item.id == item.parentId:
                    raise ValueError("A parent can't be himself")

                if dict_id.get(item.parentId):
                    if dict_id.get(item.parentId) != SystemItemType.folder:
                        raise ValueError("The parent is not a folder")
                else:
                    for session in get_db():
                        node = session.query(Node).get(item.parentId)
                        if not node:
                            raise ValueError("The parent is not found")

                        if node.type != SystemItemType.folder:
                            raise ValueError("The parent is not a folder")
        return var

    @validator("updateDate", pre=True)
    def validate_update_date(cls, var):
        if isinstance(var, str) and str_to_datetime(var):
            return var
        else:
            raise TypeError("Incorrect time format or type")


class SystemItemHistoryUnit(SystemItemImport):
    date: datetime


class SystemItemHistoryResponse(BaseModel):
    items: list[SystemItemHistoryUnit]


class Error(BaseModel):
    code: int
    message: str
