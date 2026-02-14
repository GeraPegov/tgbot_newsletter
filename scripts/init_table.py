import asyncio
from infrastructure.connection import Base, engine


async def create_table():
    async with engine.begin() as conn:
        await conn.execute(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.run(create_table())