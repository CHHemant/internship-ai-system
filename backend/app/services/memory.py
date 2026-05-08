import json

import redis
from redis import RedisError

from app.config import get_settings


class AgentMemoryStore:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = redis.from_url(settings.redis_url, decode_responses=True)

    def save(self, key: str, value: dict) -> None:
        try:
            self._client.set(key, json.dumps(value), ex=3600)
        except RedisError:
            return

    def get(self, key: str) -> dict | None:
        try:
            raw = self._client.get(key)
        except RedisError:
            return None
        return json.loads(raw) if raw else None
