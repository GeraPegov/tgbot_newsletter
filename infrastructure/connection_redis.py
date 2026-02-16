from redis.asyncio import Redis


async def get_redis():
    redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)
    yield redis
    await redis.aclose()
