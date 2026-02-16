import asyncio
from pathlib import Path
import sys

infrastructure = Path(__file__).parent.parent
sys.path.insert(0, str(infrastructure))
from infrastructure.connection_postgres import Base, engine
from infrastructure.models import message


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_table())
