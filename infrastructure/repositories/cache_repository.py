

from redis.asyncio import Redis


class UsersCache:
    def __init__(self, session: Redis):
        self.session = session

    async def _check(self, user_id: int, media_group_id: str):
        check = await self.session.get(f'{str(user_id)}:{media_group_id}')
        return True if check > 0 else False
    
    async def _delete(self, user_id: int):
        keys_to_delete = await self.session.keys(f'{user_id}:*')
        if keys_to_delete:
            await self.session.delete(*keys_to_delete)

    async def save(self, user_id: int, message: str, media_group_id: str):
        check_records = await self._check(user_id, media_group_id)
        if check_records is False:
            await self._delete(user_id)

        await self.session.rpush(f'{str(user_id)}:{media_group_id}', message.encode('utf-8'))

    async def get_message(self, user_id: int):
        data = await self.session.get(str(user_id))

    
    async def _decode(self):
        pass
    