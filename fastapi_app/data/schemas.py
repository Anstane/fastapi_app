from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DataBase(BaseModel):
    """Базовый формат входных данных."""

    device: str
    x: float
    y: float
    z: float


class DataCreate(DataBase):
    """Данные передаваемые в create."""
    
    pass


class Data(DataBase):
    """Данные для чтения."""

    model_config = ConfigDict(from_attributes=True)
    timestamp: datetime
    id: int


class DateFormat(BaseModel):
    """JSON для передачи дат."""

    start_date: datetime
    end_date: datetime
