import contextlib
from typing import Any, AsyncIterator
 
from ..core.config import settings
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
 
class Base(DeclarativeBase):
    pass
 
class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine, expire_on_commit=False)
 
    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
 
        self._engine = None
        self._sessionmaker = None
 
    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
 
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise
 
    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")
 
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
 
def conn_uri_data_to_db_sql_config():
    connection_uri = sa.engine.URL.create(
        "postgresql+asyncpg",
        username=settings.DATABASE_USERNAME,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        database=settings.DATABASE_NAME
    )
    return connection_uri
 
db_connection_url = conn_uri_data_to_db_sql_config()
sessionmanager = DatabaseSessionManager(db_connection_url, {"echo": settings.echo_sql})
 
async def get_db_session():
    async with sessionmanager.session() as session:
        yield session