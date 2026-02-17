import asyncio
from pathlib import Path
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

infrastructure = Path(__file__).parent.parent
sys.path.insert(0, str(infrastructure))

from infrastructure.config import settings


async def drop_table(db_name: str = "tgbot"):
    engine = create_async_engine(url=settings.ADMIN_DB_URL)
    async with engine.connect() as conn:
        await conn.execution_options(isolation_level="AUTOCOMMIT")
        await conn.execute(text(f"DROP DATABASE {db_name}"))


if __name__ == "__main__":
    asyncio.run(drop_table())
