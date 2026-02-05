import datetime
import uuid

from sqlalchemy import Column, DateTime, Integer, String

from database import Base


class Note(Base):
    __tablename__ = "notes"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    heading = Column(String(64))
    body = Column(String(256))
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())
