import redis
import config
import asyncio
import typing


class CacheManager:
    def __init__(self):
        self.cache = redis.Redis(
            host=config.redis_host, port=config.redis_port, db=0, decode_responses=True
        )
        asyncio.run(self.check_cache_connection())
        print("Cache connection succeeded")

    async def check_cache_connection(self):
        try:
            res = self.cache.ping()
            if asyncio.iscoroutine(res) or isinstance(res, typing.Awaitable):
                await res
            elif not res:
                print(f"Unexpected result from cache health check: {res}")
                raise redis.exceptions.ConnectionError()
        except redis.exceptions.ConnectionError:
            print("Connection to cache failed. Exiting...")
            exit()

    def put(self, key, value):
        self.cache.set(key, value, ex=config.redis_default_expiry_seconds)

    def get(self, key):
        return self.cache.get(key)
