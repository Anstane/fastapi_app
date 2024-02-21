from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_help
from .schemas import Data, DataCreate
from . import crud

router = APIRouter(tags=['Data'])


@router.get('/', response_model=list[Data])
async def get_data(
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Получаем все объекты данных."""

    return await crud.get_all_data(session=session)


@router.get('/{data_id}/', response_model=Data)
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


@router.post('/', response_model=Data)
async def post_data(
    data_in: DataCreate,
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    """Добавляем данные в БД."""

    return await crud.create_data(session=session, data_in=data_in)


@router.get('/statistics/{device}/')
async def get_statistics(
    device: str,
    session: AsyncSession = Depends(db_help.scoped_session_dependency),
):
    device_exists = await crud.check_device_exists(session=session, device=device)
    if device_exists:
        return await crud.get_statistics(session=session, device=device)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Устройство {device} не найдено.'
    )
