from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from database import Data
from .schemas import DataCreate

# Create / Read методы.

async def get_all_data(session: AsyncSession) -> list[Data]:
    """Получить все данные."""

    stmt = select(Data).order_by(Data.id) # Получаем данные и сортируем по ID.
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return data


async def create_data(session: AsyncSession, data_in: DataCreate) -> Data:
    """Опубликовать данные в БД."""

    data = Data(**data_in.model_dump())
    session.add(data)
    await session.commit() # Возможно ещё нужно session.refresh()
    return data


async def get_data(session: AsyncSession, data_id: int) -> Data | None:
    """Получить конкретные данные."""

    return await session.get(Data, data_id)


async def get_data_device(session: AsyncSession, device: str) -> list[Data]:
    """Получить данные по устройству."""

    stmt = select(Data).filter(Data.device == device)
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return data
