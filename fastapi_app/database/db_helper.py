from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from .config import settings

# Основная логика БД.

class DBHelper:
    """Класс для создания движка и запуска async сессии."""

    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        ) # Запускаем движок с данными из config.py
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        ) # Фабрика сессий.
    
    def get_scoped_session(self): # Создаём временную сессию.
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def scoped_session_dependency(self): # Функция для взаимодействия с сессией.
        session = self.get_scoped_session()
        yield session
        await session.close()

db_help = DBHelper(url=settings.db_url, echo=settings.db_echo) # Переменная для хранения объекта класса.
