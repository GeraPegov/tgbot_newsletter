import asyncio
import json
import time
import pytest
from redis.asyncio import Redis

from infrastructure.repositories.cache_repository import UsersCache


@pytest.mark.asyncio
async def test_check(get_redis, test_message_redis):
    cache = UsersCache(get_redis)

    check = await cache._check(1, "1")
    assert check is True

    check = await cache._check(1, None)
    assert check is False

    await get_redis.rpush("2:None:str", "hello")
    check = await cache._check(2, None)
    assert check is False


@pytest.mark.asyncio
async def test_delete(get_redis, test_message_redis):
    cache = UsersCache(get_redis)
    key = await get_redis.keys("1:*")
    assert len(key) == 1

    await cache._delete(1)
    key = await get_redis.keys("1:*")
    assert len(key) == 0


@pytest.mark.asyncio
async def test_save(get_redis: Redis):
    cache = UsersCache(get_redis)
    await cache.save(user_id=1, message="text", media_group_id=None, message_type="str")
    message = await get_redis.lrange("1:None:str", 0, -1)
    result = json.loads(message[0])
    assert result["message"] == "text"
    assert result["type"] == "str"
    ttl_base = await get_redis.ttl("1:None:str")
    assert ttl_base == 3600
    await asyncio.sleep(2)
    ttl = await get_redis.ttl("1:None:str")
    assert ttl == ttl_base - 2


@pytest.mark.asyncio
async def test_get_message(get_redis, test_message_redis):
    cache = UsersCache(get_redis)

    message = await cache.get_message(1)

    assert isinstance(message, list)
    assert isinstance(message[0], list)
    assert message[0][0] == "text"
    assert message[0][1] == "str"
