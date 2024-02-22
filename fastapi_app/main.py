from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, db_help
from data import router as router_v1

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    События цикла жизни приложения.
    
    При запуске создается объекты базы данных.
    """

    async with db_help.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router_v1)
