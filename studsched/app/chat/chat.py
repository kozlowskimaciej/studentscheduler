import asyncio
import logging
from typing import Iterable, Optional

from redis import asyncio as aioredis

from ..configs import get_settings
from .models.models import *

settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)


class RedisChatService:
    def __init__(self, url: str):
        self.redis = aioredis.from_url(url, decode_responses=True, encoding="utf-8")

    def close(self):
        asyncio.create_task(self.redis.close())
        asyncio.create_task(self.redis.connection_pool.disconnect())

    async def get_channels(self) -> Iterable[Channel]:
        channels = await self.redis.hgetall(":channels")
        return (Channel(slug=slug, name=name) for slug, name in channels.items())

    async def get_channel(self, slug: str) -> Optional[Channel]:
        name = await self.redis.hget(":channels", slug)
        if not name:
            return None
        return Channel(name=name, slug=slug)

    async def create_channel(self, slug: str, name: str) -> Channel:
        await self.redis.hset(":channels", mapping={slug: name})
        return Channel(name=name, slug=slug)

    async def get_messages(self, channel_slug: str) -> Iterable[Message]:
        redis_stream: str = f":channel-{channel_slug}:messages"
        response = dict(await self.redis.xread({redis_stream: "0-0"}, count=1))
        stream_messages = response.get(redis_stream, [])
        return [
            Message.parse_raw(payload["data"]) for _msg_id, payload in stream_messages
        ]

    async def send_message(
        self, channel_slug: str, user: UserBase, message_base: MessageBase
    ) -> Message:
        message = Message(
            **message_base.dict(),
            sender_username=user.username,
            channel_slug=channel_slug,
        )
        await self.redis.xadd(
            f":channel-{channel_slug}:messages", id="*", fields={"data": message.json()}
        )
        return message

    async def incoming_messages(
        self, channel_slug: str, read_timeout: float = None, only_new: bool = False
    ):
        redis_channel = f":channel-{channel_slug}:messages"
        last_msg = "0-0"
        block_time = None
        if read_timeout is not None:
            block_time = read_timeout * 1000
        while True:
            if messages := await self.redis.xread(
                {redis_channel: last_msg}, count=1, block=block_time
            ):
                last_msg, message_serialized = dict(messages)[redis_channel][0]
                message = Message.parse_raw(message_serialized["data"])
                yield message
            else:
                yield ...


def create_chat_service(url: str):
    return RedisChatService(url)
