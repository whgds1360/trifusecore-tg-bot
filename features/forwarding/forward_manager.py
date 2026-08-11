from aiovk import API, TokenSession
from aiovk.longpoll import BotsLongPoll

from aiogram import Bot
from loguru import logger
from asyncio import Task, CancelledError
from typing import final, Dict


@final
class ForwardManager:

    @staticmethod
    async def vk_listener(
        bot: Bot,
        chat_id: int,
        vk_token: str,
        vk_community_token: str,
        active_listeners: Dict[int, Task]
    ):

        try:
            async with TokenSession(access_token=vk_token) as token_session:
                api = API(token_session)
                group_id = int(vk_community_token)
                longpoll = BotsLongPoll(session_or_api=api, group_id=group_id)

                async for event in longpoll.iter():
                    if chat_id not in active_listeners:
                        break

                    if event.get("type") == 'message_new':
                        msg = event.get("object").get("message")

                        if msg:
                            text = msg.get('text', '')

                            if text:
                                try:
                                    user_info = await api.users.get(
                                        user_ids=[msg['from_id']],
                                        fields=['first_name', 'last_name']
                                    )
                                    if user_info:
                                        user = user_info[0]
                                        name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(
                                        )

                                        await bot.send_message(
                                            chat_id=chat_id,
                                            text=f"💬 Новое сообщение от {name}:\n{text}"
                                        )

                                except Exception as error:
                                    logger.error(
                                        f"Не удалось получить имя при перессылке: {error}")

        except CancelledError:
            pass

        except Exception as error:
            logger.error(f"Ошибка в слушателе: {error}")

        finally:
            task = active_listeners.pop(chat_id, None)

            if task and not task.done():
                task.cancel()
