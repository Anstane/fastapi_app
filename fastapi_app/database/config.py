from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки БД."""

    db_url: str = 'sqlite+aiosqlite:///database/db.sqlite3'
    db_echo: bool = True

settings = Settings()
