import asyncio
import logging
from redis import asyncio as aioredis
from ..configs import get_settings

settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)


class RedisChatService:
    def __init__(self, url: str):
        self.redis = aioredis.from_url(
            url, decode_responses=True, encoding="utf-8"
        )
        super().__init__()

    def close(self):
        asyncio.create_task(self.redis.close())
        asyncio.create_task(self.redis.connection_pool.disconnect())
        logger.info("Redis connection closed.")


def create_chat_service(url: str):
    return RedisChatService(url)
