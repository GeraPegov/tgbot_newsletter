import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from infrastructure.config import settings

async def create_db():
    engine = create_async_engine(
        url=settings.DB_URL
    )

    async with engine.begin() as conn:
        await conn.execution_options(isolation_level='AUTOCOMMIT')
        await conn.execute(text("CREATE DATABASE tgbot"))
    

if __name__ == '__main__':
    asyncio.run(create_db())