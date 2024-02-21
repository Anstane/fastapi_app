from datetime import datetime
from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Data(Base):
    """Модель данных для взаимодействия."""

    __tablename__ = 'data'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    device: str = Column(String, index=True)
    timestamp: datetime = Column(DateTime, index=True, default=datetime.utcnow)
    x: float = Column(Float)
    y: float = Column(Float)
    z: float = Column(Float)
