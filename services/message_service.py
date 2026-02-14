

from io import BytesIO
from aiogram import Bot
from infrastructure.repositories.cache_repository import UsersCache
from infrastructure.repositories.message_repository import UsersMessageRepository


class UsersMessageService:
    def __init__(self, repo: UsersMessageRepository, cache: UsersCache):
        self.repo = repo
        self.cache = cache

    async def download_file(self, file_id: str, bot: Bot):
        file = await bot.get_file(file_id)
        photo_io = BytesIO()
        await bot.download_file(file.file_path, photo_io)
        return photo_io.getvalue()

    async def save_messages(
            self,
            message,
            user_id,
            media_group_id,
            message_type
            ):
        result = await self.repo.save(
            message,
            user_id,
            media_group_id,
            message_type
            )
        await self.cache.save(message, user_id, media_group_id)
        return result 

    async def get_messages(self, user_id):
        data = self.cache.get_message(user_id)
        if data:
            return data
        return await self.repo.get_message(user_id)
        

