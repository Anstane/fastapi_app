from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from database import Data
from .schemas import DataCreate


async def get_all_data(session: AsyncSession) -> list[Data]:
    """Получить все данные."""

    stmt = select(Data).order_by(Data.id) # Получаем данные и сортируем по ID.
    result: Result = await session.execute(stmt)
    data = result.scalars().all()
    return data


async def get_data(session: AsyncSession, data_id: int) -> Data | None:
    """Получить конкретные данные."""

    return await session.get(Data, data_id)


async def create_data(session: AsyncSession, data_in: DataCreate) -> Data:
    """Опубликовать данные в БД."""

    data = Data(**data_in.model_dump())
    session.add(data)
    await session.commit() # Возможно ещё нужно session.refresh()
    return data


async def check_device_exists(session: AsyncSession, device: str) -> bool:
    """Проверяем, что устройство есть в БД."""

    stmt = select(Data).where(Data.device == device)
    result: Result = await session.execute(stmt)
    device_obj = result.scalars().first()
    return device_obj is not None


async def get_parameter_statistics(session: AsyncSession, column, device: str) -> dict:
    """Получаем статистику по полю."""

    stmt = select(
        func.min(column),
        func.max(column),
        func.count(column),
        func.sum(column),
    ).where(
        Data.device == device
    ) # Получаем доступные данные через агрегирующие функции.

    result = await session.execute(stmt)
    statistics = result.first()

    # Функция median() отсутствует, поэтому реализуем её сами.
    values = await session.execute(select(column).where(Data.device == device))
    values = [v[0] for v in values.all()] # Получаем список значений по устройству.

    median_value = None
    if values: # Сортируем значения и находим центральное.
        sorted_values = sorted(values)
        n = len(sorted_values)
        if n % 2 == 0:
            median_value = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
        else:
            median_value = sorted_values[n // 2]

    return {
        "min": statistics[0],
        "max": statistics[1],
        "count": statistics[2],
        "sum": statistics[3],
        "median": median_value,
    }


async def get_statistics(session: AsyncSession, device: str) -> dict:
    """Передаём параметры для высчитывания статистики."""

    statistics_x = await get_parameter_statistics(session, Data.x, device)
    statistics_y = await get_parameter_statistics(session, Data.y, device)
    statistics_z = await get_parameter_statistics(session, Data.z, device)

    return {
        "x": statistics_x,
        "y": statistics_y,
        "z": statistics_z
    }
