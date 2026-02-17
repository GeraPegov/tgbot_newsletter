import asyncio
from pathlib import Path
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

infrastructure = Path(__file__).parent.parent
sys.path.insert(0, str(infrastructure))

from infrastructure.config import settings


async def create_db(db_name: str = "tgbot", test_db_name: str = "testtgbot"):
    engine = create_async_engine(url=settings.ADMIN_DB_URL)

    async with engine.connect() as conn:
        await conn.execution_options(isolation_level="AUTOCOMMIT")
        result = await conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": db_name},
        )
        exists = result.scalar_one_or_none()
        if not exists:
            await conn.execute(text(f"CREATE DATABASE {db_name}"))


if __name__ == "__main__":
    asyncio.run(create_db())
