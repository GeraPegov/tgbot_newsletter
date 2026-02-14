

from infrastructure.repositories.cache_repository import UsersCache
from infrastructure.repositories.message_repository import UsersMessageRepository


class UsersMessageService:
    def __init__(self, repo: UsersMessageRepository, cache: UsersCache):
        self.repo = repo
        self.cache = cache

    async def save_messages(self, messages, user_id):
        result = await self.repo.save(messages, user_id)
        await self.cache.save(messages, user_id)
        return result 

    async def get_messages(self, user_id):
        data = self.cache.get_message(user_id)
        if not data:
            return await self.repo.get_message(user_id)
        return data

