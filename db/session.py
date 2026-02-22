# db/session.py — рекомендую этот на старте

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///db/tattoo.db"
engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    """Возвращает новую сессию. Использовать так: async with (await get_async_session()) as session:"""
    return async_session_maker()
