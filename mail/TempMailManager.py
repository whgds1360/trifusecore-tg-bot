from temp_mails import Tenminemail_com
from loguru import logger
from typing import final, Optional


@final
class TempMailManager:

    def __init__(self) -> None:
        try:
            self.email = Tenminemail_com()
        except Exception as error:
            logger.info(f"Ошибка инициализации временой почты: {error}")

    def get_inbox(self) -> Optional[str]:
        try:
            result = ""
            messages = self.email.get_inbox()
            if messages:
                for msg in messages:
                    from_addr = msg.get('from', 'Неизвестно')
                    subject = msg.get('subject', 'Пусто')
                    msg_id = msg.get('id')

                    try:
                        if msg_id:
                            content = self.email.get_mail_content(mail_id=msg_id)
                            if content:
                                if len(content) > 500:
                                    content = content[:500] + "...\n(текст обрезан)"
                                result += (f"📧От кого:\n{from_addr}\n📝Тема:\n{subject}\n\n📜Содержание:\n{content}")

                    except Exception as error:
                        logger.error(f"Не удалось получить содержимое письма: {error}")

                return result
        except Exception as error:
            logger.error(f"Ошибка при получении писем: {error}")
        return "Пусто"