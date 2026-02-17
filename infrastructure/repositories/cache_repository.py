import json
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import TimeoutError as RedisTimeoutError

P = ParamSpec("P")
T = TypeVar("T")


def handle_redis_error(
    func: Callable[P, Awaitable[T]],
) -> Callable[P, Awaitable[T | Any]]:
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (RedisConnectionError, RedisTimeoutError):
            return None

    return wrapper


class UsersCache:
    def __init__(self, session: Redis):
        self.session = session

    @handle_redis_error
    async def _check(self, user_id: int, media_group_id: str | None):
        key = await self.session.keys(f"{str(user_id)}:{media_group_id}:*")
        return True if len(key) > 0 and key[0].split(":")[1] != "None" else False

    @handle_redis_error
    async def _delete(self, user_id: int):
        keys_to_delete = await self.session.keys(f"{str(user_id)}:*")
        if keys_to_delete:
            await self.session.delete(*keys_to_delete)

    @handle_redis_error
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

    @handle_redis_error
    async def get_messages(self, user_id: int):
        key = await self.session.keys(f"{str(user_id)}:*")
        if len(key) == 0:
            return None
        records = await self.session.lrange(key[0], 0, -1)

        messages = []

        for record in records:
            data = json.loads(record)
            message = [data["message"], data["type"]]
            messages.append(message)

        return messages
