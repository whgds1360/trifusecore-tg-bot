from aiovk import API, TokenSession
from aiovk.longpoll import BotsLongPoll

from aiogram import Bot

from loguru import logger

from typing import final, List


@final
class ForwardManager:

    @staticmethod
    async def vk_listener(
        bot: Bot,
        chat_id: int,
        vk_token: str,
        vk_community_token: str,
        list_of_listen: str,
        active_listeners: List[int]
    ):

        try:
            session = TokenSession(access_token=vk_token)
            api = API(session)

            group_id = int(vk_community_token)

            longpoll = BotsLongPoll(session_or_api=api, group_id=group_id)

            ready_list_of_listen = [int(x.strip()) for x in list_of_listen.split(",") if x.strip()]

            async for event in longpoll.iter():
                if event.type == 'message_new':
                    msg = event.object.message

                    if msg:
                        text = msg.get('text', '')
                        peer_id = msg.get('peer_id')

                        if text and peer_id in ready_list_of_listen:
                            try:

                                user_info = await api.users.get(
                                    user_ids=[msg['from_id']],
                                    fields=['first_name', 'last_name']
                                )
                                if user_info:
                                    user = user_info[0]
                                    name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()

                                    await bot.send_message(
                                        chat_id=chat_id,
                                        text=f"💬 Новое сообщение от {name}:\n{text}"
                                    )

                            except Exception as e:
                                logger.warning(f"Не удалось получить имя пользователя: {e}")

        except Exception as e:
            if chat_id in active_listeners:
                active_listeners.remove(chat_id)
            logger.error(f"❌ Ошибка в слушателе: {e}")
            await bot.send_message(
                chat_id=chat_id,
                text="❌ Ваш конфиг не корректный!"
            )
        finally:
            if chat_id in active_listeners:
                active_listeners.remove(chat_id)
                logger.info(f"⏹️ Слушатель для чата {chat_id} завершён")
