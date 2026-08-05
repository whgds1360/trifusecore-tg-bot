from tempmail import AsyncTempMailClient, EmailAddress
from resources.ResourcesManager import ResourcesManager

from loguru import logger
from typing import final, Optional, ClassVar


@final
class TempMailManager:

    __client: ClassVar[AsyncTempMailClient]

    @classmethod
    def init_client(cls) -> None:
        cls.__client = AsyncTempMailClient(api_key=ResourcesManager.TEMP_MAIL_API_KEY)

    @classmethod
    async def make_mail(cls) -> Optional[EmailAddress]:
        try:
            async with cls.__client as client:
                email = await client.create_email()
                return email
        except Exception as error:
            logger.error(f"Ошибка создания временной почты {error}")
        return None

    @classmethod
    async def get_mails(cls, email: EmailAddress) -> Optional[str]:
        try:
            async with cls.__client as client:
                result = ""
                messages = await client.list_email_messages(email.email)
                if messages:
                    for msg in messages:
                        result += (f"📧От кого:\n{msg.from_addr}\n\n📝Тема:\n{msg.subject}\n\n\n")
                    return result
        except Exception as error:
            logger.error(f"Ошибка при получении писем: {error}")
        return None
