from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_help
from .schemas import Data, DataCreate, DateFormat
from . import crud
from . import statistic

router = APIRouter(tags=['Data'])


@router.get('/', response_model=list[Data])
async def get_data(
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Получаем все объекты данных."""

    return await crud.get_all_data(session=session)


@router.post('/', response_model=Data)
async def post_data(
    data_in: DataCreate,
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Добавляем данные в БД."""

    return await crud.create_data(session=session, data_in=data_in)


@router.get('/data_id/{data_id}/', response_model=Data)
async def get_data_obj(
    data_id: int,
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Получаем один конкретный объект данных."""

    data = await crud.get_data(session=session, data_id=data_id)
    if data:
        return data

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Данные не существуют.'
    )


@router.get('/device/{device}/', response_model=list[Data])
async def get_data_device(
    device: str,
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Получаем все данные передавая устройство."""

    device_exists = await statistic.check_device_exists(session=session, device=device)
    if device_exists:
        return await crud.get_data_device(session=session, device=device)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Устройство {device} не найдено.'
    )


@router.post('/statistics/')
async def get_statistics_date(
    dates: DateFormat,
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Высчитываем статистику по устройству за указанный временной период."""

    return {
        dates.end_date,
        dates.start_date
    }


@router.get('/statistics/{device}/')
async def get_statistics_device(
    device: str,
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Получаем статистику по устройству за всё время."""

    device_exists = await statistic.check_device_exists(session=session, device=device)
    if device_exists:
        return await statistic.get_statistics(session=session, device=device)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Устройство {device} не найдено.'
    )
