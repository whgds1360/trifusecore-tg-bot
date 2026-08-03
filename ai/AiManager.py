from typing import final, ClassVar, Optional
from groq import AsyncGroq
from resources.ResourcesManager import ResourcesManager
from loguru import logger


@final
class AiManager:

    client: ClassVar = AsyncGroq(api_key=ResourcesManager.AI_API_KEY)

    @classmethod
    async def get_response(cls, content: str) -> Optional[str]:
        chat_completion = await cls.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
