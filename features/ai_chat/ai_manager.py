from typing import final, ClassVar, Optional
from groq import AsyncGroq
from core.resources_manager import ResourcesManager


@final
class AiManager:
    """Управляет взаимодействием с нейросетью через API Groq."""

    client: ClassVar = AsyncGroq(api_key=ResourcesManager.AI_API_KEY)

    @classmethod
    async def get_response(cls, content: str) -> Optional[str]:
        """Отправляет запрос к нейросети и возвращает ответ.

        Args:
            content: Текст запроса пользователя.

        Returns:
            Optional[str]: Ответ нейросети или None при ошибке.
        """
        chat_completion = await cls.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            model=ResourcesManager.AI_MODEL,
        )

        return chat_completion.choices[0].message.content
