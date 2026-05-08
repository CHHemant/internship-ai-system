import json

import redis

from app.config import get_settings


class AgentMemoryStore:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = redis.from_url(settings.redis_url, decode_responses=True)

    def save(self, key: str, value: dict) -> None:
        self._client.set(key, json.dumps(value), ex=3600)

    def get(self, key: str) -> dict | None:
        raw = self._client.get(key)
        return json.loads(raw) if raw else None
