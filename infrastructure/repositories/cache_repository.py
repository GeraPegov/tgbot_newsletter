

from redis.asyncio import Redis


class UsersCache:
    def __init__(self, session: Redis):
        self.session = session


    async def save(self, user_id: int, objects: list):
        if await self.session.get(str(user_id)) is not None:
            await self.session.delete(str(user_id))

        await self.session.rpush(str(user_id), *objects)

    async def get_message(self, user_id: int):
        return await self.session.get(str(user_id))
    