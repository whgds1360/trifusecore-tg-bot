from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from typing import final


@final
class KeyboardCreator():
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🌐 ВК -> TG пересылка", callback_data="forward_menu"),
                    InlineKeyboardButton(text="✉️ Временная почта", callback_data="temp_mail_menu"),
                    InlineKeyboardButton(text="🤖 Нейро", callback_data="ai_menu")
                ],
                [
                    InlineKeyboardButton(text="ℹ️ Инфо", callback_data="main_info")
                ],
                [
                    InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
                ]
            ]
        )

    @staticmethod
    def forward_menu() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="✅ Начать", callback_data="begin_forward"),
                            InlineKeyboardButton(text="❌ Остановить", callback_data="end_forward"),
                        ],
                        [
                            InlineKeyboardButton(text="⚙️ Установить конфиг", callback_data="config_forward"),
                            InlineKeyboardButton(text="❌ Удалить существующий", callback_data="delete_forward_config"),
                        ],
                        [
                            InlineKeyboardButton(text="ℹ️ Инфо", callback_data="info_forward")
                        ],
                        [
                            InlineKeyboardButton(text="↩️ Назад", callback_data="back_forward")
                        ]
                    ]
                )

    @staticmethod
    def ai_mod_menu() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="🧠 Ответ на вопросы", callback_data="change_mod_request"),
                            InlineKeyboardButton(text="📷 Генерация фото", callback_data="change_mod_photo"),
                        ],
                        [
                            InlineKeyboardButton(text="ℹ️ Инфо", callback_data="info_ai_mod")
                        ],
                        [
                            InlineKeyboardButton(text="↩️ Назад", callback_data="back_ai_mod")
                        ]
                    ]
                    )
