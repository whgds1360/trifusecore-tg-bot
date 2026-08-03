from typing import final, ClassVar, Optional
from groq import AsyncGroq


@final
class AiManager:

    client: ClassVar = AsyncGroq()

    @classmethod
    async def get_response(cls, content: str) -> Optional[str]:
        chat_completion = await cls.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            model="llama3-70b-8192",
        )
        return chat_completion.choices[0].message.content
