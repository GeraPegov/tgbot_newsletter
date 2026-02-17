import json
from redis.asyncio import Redis


class UsersCache:
    def __init__(self, session: Redis):
        self.session = session

    async def _check(self, user_id: int, media_group_id: str | None):
        key = await self.session.keys(f"{str(user_id)}:{media_group_id}:*")
        return True if len(key) > 0 and key[0].split(":")[1] != "None" else False

    async def _delete(self, user_id: int):
        keys_to_delete = await self.session.keys(f"{str(user_id)}:*")
        if keys_to_delete:
            await self.session.delete(*keys_to_delete)

    async def save(
        self, user_id: int, message: str, media_group_id: str | None, message_type: str
    ):
        check_records = await self._check(user_id, media_group_id)
        if check_records is False:
            await self._delete(user_id)
        data = json.dumps({"message": message, "type": message_type})
        await self.session.rpush(
            f"{str(user_id)}:{media_group_id}:{message_type}", data
        )
        await self.session.expire(
            f"{str(user_id)}:{media_group_id}:{message_type}", 3600
        )

    async def get_message(self, user_id: int):
        key = await self.session.keys(f"{str(user_id)}:*")

        records = await self.session.lrange(key[0], 0, -1)

        list_of_lists_with_messages = []

        for record in records:
            data = json.loads(record)
            message_list = [data["message"], data["type"]]
            list_of_lists_with_messages.append(message_list)

        return list_of_lists_with_messages
