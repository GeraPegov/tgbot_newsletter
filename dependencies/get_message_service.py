
from infrastructure.connection_postgres import get_db
from infrastructure.repositories.cache_repository import UsersCache
from infrastructure.repositories.message_repository import UsersMessageRepository
from services.message_service import UsersMessageService
from infrastructure.connection_redis import get_redis

def get_cache():
    session = get_redis()
    return UsersCache(session)

def get_repo():
    session = get_db()
    return UsersMessageRepository(session)

def get_message_service():
    repo = get_repo()
    cache = get_cache()
    return UsersMessageService(repo, cache)