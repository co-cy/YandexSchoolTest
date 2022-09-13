from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from MyDisk.schemas.item_type import SystemItemType
from MyDisk.database import Base


class Node(Base):
    __tablename__ = "node"

    id = Column(String(256), primary_key=True, unique=True, index=True, nullable=False)

    parentId = Column(String, ForeignKey("node.id"), default=None, nullable=True)
    children: list = relationship("Node", cascade="all, delete")

    type = Column(String(32), nullable=False)

    url = Column(String(255), default=None, nullable=True)
    size = Column(Integer, default=None, nullable=True)

    date = Column(DateTime, nullable=False, index=True)

    def json(self) -> dict:
        json = {
            "id": self.id,
            "parentId": self.parentId,
            "type": self.type,
            "url": self.url,
            "size": self.size,
            "date": self.date
        }

        if self.type == SystemItemType.folder:
            json["children"] = [child.json() for child in self.children]

        return json
