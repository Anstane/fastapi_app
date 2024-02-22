from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from database import Data
from .schemas import DateDevice

# Логика для взимодействия со статистикой.

async def get_data_by_device(session: AsyncSession, device: str) -> list[Data]:
    """Получаем все записи по устройству."""

    stmt = select(Data).where(Data.device == device)
    result: Result = await session.execute(stmt)
    data = result.scalars().all()

    return data


async def get_data_by_date_and_device(session: AsyncSession, data_in: DateDevice) -> list[Data]:
    """Эта функция подготавливает данные под условия по дате и устройству."""

    # Форматируем полученную строку от пользователя в формате YY-MM-DD
    start_date = datetime.strptime(data_in.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(data_in.end_date, '%Y-%m-%d')

    stmt = (
        select(Data)
        .filter(
            and_(
                Data.timestamp >= start_date,
                Data.timestamp <= end_date,
                Data.device == data_in.device
            )
        )
    )

    result: Result = await session.execute(stmt)
    data = result.scalars().all()

    return data


async def get_parameter_statistics(data: list[Data], column) -> dict:
    """Подсчитываем статистику полученной выборки по полю."""

    values = [getattr(item, column.key) for item in data] # Генератор получающий атрибуты по полю.

    min_value = min(values)
    max_value = max(values)
    count = len(values)
    sum_value = sum(values)

    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 0:
        median_value = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    else:
        median_value = sorted_values[n // 2]

    return {
        "min": min_value,
        "max": max_value,
        "count": count,
        "sum": sum_value,
        "median": median_value,
    }


async def get_statistics(data: list[Data]) -> dict:
    """Передаём поля и данные для высчитывания статистики."""

    statistics_x = await get_parameter_statistics(data, Data.x)
    statistics_y = await get_parameter_statistics(data, Data.y)
    statistics_z = await get_parameter_statistics(data, Data.z)

    return {
        "x": statistics_x,
        "y": statistics_y,
        "z": statistics_z
    }
