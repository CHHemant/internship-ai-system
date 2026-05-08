import logging

from openai import OpenAI

from app.config import get_settings

logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self) -> None:
        settings = get_settings()
        self._model = settings.openai_model
        self._client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        if not self._client:
            logger.warning("OPENAI_API_KEY not configured; using deterministic fallback generation")
            return f"{system_prompt}\n\n{user_prompt}"

        response = self._client.chat.completions.create(
            model=self._model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or ""
