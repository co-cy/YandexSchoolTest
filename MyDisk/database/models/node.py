from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from MyDisk.schemas.item_type import SystemItemType
from MyDisk.helper import str_to_datetime
from MyDisk.database import Base


class Node(Base):
    __tablename__ = "node"

    id = Column(String(256), primary_key=True, unique=True, index=True, nullable=False)

    parentId = Column(String, ForeignKey("node.id"), default=None, nullable=True)
    children: list = relationship("Node", cascade="all, delete")

    type = Column(String(32), index=True, nullable=False)

    url = Column(String(255), default=None, nullable=True)
    size = Column(Integer, default=0, nullable=False)

    date_string = Column(String(64), nullable=False)
    date = Column(DateTime, nullable=False, index=True)

    def json(self) -> dict:
        json = {
            "id": self.id,
            "parentId": self.parentId,
            "children": None,
            "type": self.type,
            "url": self.url,
            "size": self.size,
            "date": self.date_string
        }

        if self.type == SystemItemType.folder:
            json["children"] = [child.json() for child in self.children]

        return json

    def update(self, params: dict, date: str):
        if self.type == SystemItemType.file:
            if params.get("id"):
                self.id = params.get("id")
            if params.get("parentId"):
                self.parentId = params.get("parentId")
            if params.get("type"):
                self.type = params.get("type")
            if params.get("url"):
                self.url = params.get("url")
            if params.get("size"):
                self.size = params.get("size")
        elif self.type == SystemItemType.folder:
            if params.get("id"):
                self.id = params.get("id")
            if params.get("parentId"):
                self.parentId = params.get("parentId")
            if params.get("type"):
                self.type = params.get("type")

        self.date = str_to_datetime(date)
        self.date_string = date
