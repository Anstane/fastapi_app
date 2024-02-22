from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_help
from .schemas import Data, DataCreate, DateDevice
from . import crud
from . import statistic

router = APIRouter(tags=['Data'])


@router.get('/', response_model=list[Data])
async def get_data(
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Получаем все объекты данных."""

    data =  crud.get_all_data(session=session)
    if data:
        return data
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='База данных пуста.'
    )


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
        detail='Данные не существуют.'
    )


@router.get('/device/{device}/', response_model=list[Data])
async def get_data_device(
    device: str,
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Получаем все данные передавая устройство."""

    data = await statistic.get_data_by_device(session=session, device=device)
    if data:
        return data

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Записей по устройству {device} не найдено.'
    )


@router.post('/statistics/')
async def get_statistics_date(
    date_device: DateDevice,
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Высчитываем статистику по устройству за указанный временной период."""

    data = await statistic.get_data_by_date_and_device(session=session, data_in=date_device)
    if data:
        return await statistic.get_statistics(data)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Данные по атрибутам не существуют.'
    )


@router.get('/statistics/{device}/')
async def get_statistics_device(
    device: str,
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Получаем статистику по устройству за всё время."""

    data = await statistic.get_data_by_device(session=session, device=device)
    if data:
        return await statistic.get_statistics(data)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Записей по устройству {device} не найдено.'
    )
