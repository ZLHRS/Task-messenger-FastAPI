import json
from typing import Any
import redis.asyncio as aioredis
from core.config import redis_url

r = aioredis.from_url(redis_url, decode_responses=True)


async def get_redis(key: str):
    product = await r.get(key)
    if product is None:
        return None
    return json.loads(product)


async def get_or_set(key: str, ttl: int, data) -> Any:
    product = await r.get(key)
    if product:
        return json.loads(product)
    await r.setex(key, ttl, json.dumps(data))
    return data


async def delete_from_redis(key):
    product = await r.get(key)
    if product:
        await r.delete(key)


async def update_redis(key, data):
    await delete_from_redis(key)
    await r.setex(key, 300, json.dumps(data))
