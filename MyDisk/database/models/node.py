from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from MyDisk.database import Base


class Node(Base):
    __tablename__ = "node"

    id = Column(String, primary_key=True, unique=True, index=True, nullable=False)

    parentID = Column(String, ForeignKey("node.id"), default=None, nullable=True)
    children = relationship("Node", cascade="all, delete")

    type = Column(String(32), nullable=False)

    url = Column(String(255), default=None, nullable=True)
    size = Column(Integer, default=None, nullable=True)

    date = Column(DateTime, nullable=False, index=True)
