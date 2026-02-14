from fastapi import Depends
from infrastructure.connection_postgres import get_db
from infrastructure.repositories.cache_repository import UsersCache
from infrastructure.repositories.message_repository import UsersMessageRepository
from services.message_service import UsersMessageService
from sqlalchemy.ext.asyncio import AsyncSession

from redis.asyncio import Redis
from infrastructure.connection_redis import get_redis

def get_cache(session: Redis = Depends(get_redis)):
    return UsersCache(session)

def get_repo(session: AsyncSession = Depends(get_db)):
    return UsersMessageRepository(session)

def get_message_service(
        repo: UsersMessageRepository = Depends(get_repo),
        cache: UsersCache = Depends(get_cache)
        ):
    return UsersMessageService(repo, cache)