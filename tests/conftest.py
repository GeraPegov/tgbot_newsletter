
import json
from pathlib import Path
import sys
import pytest_asyncio
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import pytest
infrastructure = Path(__file__).parent.parent
sys.path.insert(0, str(infrastructure))
from infrastructure.config import settings
from infrastructure.connection_postgres import Base
from infrastructure.models.message import UsersMessageModel


@pytest_asyncio.fixture(scope='function')
async def engine(test_database: str = 'testtgbot'):
    admin_engine=create_async_engine(
        url=settings.ADMIN_DB_URL
    )

    async with admin_engine.connect() as conn:
        await conn.execution_options(isolation_level='AUTOCOMMIT')
        await conn.execute(text(f'DROP DATABASE IF EXISTS {test_database}'))
        await conn.execute(text(f'CREATE DATABASE {test_database}'))

    engine=create_async_engine(
        url=settings.TEST_DB_URL,
        echo=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # async with admin_engine.connect() as conn:
    #     await conn.execution_options(isolation_level="AUTOCOMMIT")
    #     await conn.execute(text(f'DROP DATABASE {test_database}'))
    
    await engine.dispose()
    

@pytest_asyncio.fixture(scope='function')
async def async_session(engine):
    async_session = async_sessionmaker(
        engine, class_=AsyncSession
    )

    async with async_session() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture(scope='function')
async def get_redis():
    redis = Redis(
        host='localhost',
        port=6379,
        db=2,
        decode_responses=True
    )
    yield redis
    await redis.flushall()
    await redis.aclose()



@pytest_asyncio.fixture
async def test_message_postgres(async_session):
    test_message = UsersMessageModel(
        user_id=1,
        media_group_id='1',
        message='hello',
        message_type='str'
    )
    async_session.add(test_message)
    await async_session.commit()
    await async_session.refresh(test_message)
    return test_message

@pytest_asyncio.fixture
async def test_message_redis(get_redis):
    message = json.dumps({'message': 'text', 'type': 'str'})
    await get_redis.rpush('1:1:str', message)

