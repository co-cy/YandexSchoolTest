from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class SystemItemType(str, Enum):
    file = "FILE"
    folder = "FOLDER"


class SystemItem(BaseModel):
    id: str
    url: str | None
    parentId: str | None
    size: int
    type: SystemItemType


class SystemItemImport(SystemItem):
    pass


class SystemItemImportRequest(BaseModel):
    items: list[SystemItemImport]
    updateDate: str


class SystemItemHistoryUnit(SystemItemImport):
    date: datetime


class SystemItemHistoryResponse(BaseModel):
    items: list[SystemItemHistoryUnit]


class Error(BaseModel):
    code: int
    message: str
