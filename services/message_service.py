from infrastructure.repositories.cache_repository import UsersCache
from infrastructure.repositories.message_repository import UsersMessageRepository


class UsersMessageService:
    def __init__(self, repo: UsersMessageRepository, cache: UsersCache):
        self.repo = repo
        self.cache = cache

    async def save_messages(
        self, message: str, user_id: int, media_group_id: str, message_type: str
    ):
        result = await self.repo.save(message, user_id, media_group_id, message_type)
        await self.cache.save(user_id, message, media_group_id, message_type)
        return result

    async def get_messages(self, user_id):
        messages = await self.cache.get_message(user_id)
        if messages:
            return messages
        return await self.repo.get_message(user_id)

    async def get_users(self):
        return await self.repo.get_users()
