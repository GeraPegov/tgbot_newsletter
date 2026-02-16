from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from infrastructure.config import settings

engine = create_async_engine(url=settings.DB_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
        await session.close()
