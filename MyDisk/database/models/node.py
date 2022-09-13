from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from MyDisk.database import Base
from datetime import datetime


class Node(Base):
    __tablename__ = "node"

    id: str = Column(String, primary_key=True, unique=True, index=True, nullable=False)

    parentID: str = Column(String, ForeignKey("node.id"), default=None, nullable=True)
    children: list = relationship("node")

    type: str = Column(String(32), nullable=False)

    url: str = Column(String(255), default=None, nullable=True)
    size: int = Column(BigInteger, default=None, nullable=True)

    date: datetime = Column(DateTime, nullable=False, index=True)
