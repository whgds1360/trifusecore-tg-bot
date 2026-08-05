from secmail import AsyncClient

from loguru import logger
from typing import final, Optional, ClassVar


@final
class TempMailManager:

    __client: ClassVar[AsyncClient]

    @classmethod
    def init_client(cls) -> None:
        cls.__client = AsyncClient()

    @classmethod
    def make_mail(cls) -> Optional[str]:
        try:
            email = cls.__client.random_email(amount=1)
            return email[0]
        except Exception as error:
            logger.error(f"Ошибка создания временной почты {error}")
        return None

    @classmethod
    async def get_mails(cls, email: str) -> Optional[str]:
        try:
            result = ""
            messages = await cls.__client.get_inbox(email)
            if messages:
                for msg in messages:
                    result += (f"📧От кого:\n{msg.from_address}\n\n📝Тема:\n{msg.subject}\n")
                return result
        except Exception as error:
            logger.error(f"Ошибка при получении писем: {error}")
        return None
