from aiogram import Bot
from aiogram.types import (
BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,
KeyboardButton, ReplyKeyboardRemove
)

from lexicon import lang_ru_menu, lang_ru_inline_buttons, lang_ru_reply_buttons


class BotMainMenuButton:
    menu_button = [
        BotCommand(command='/start', description=lang_ru_menu['button_start']),
        BotCommand(command='/help', description=lang_ru_menu['button_help'])
    ]

    @staticmethod
    async def set_commands(bot: Bot):
        await bot.set_my_commands(BotMainMenuButton.menu_button)


class BotInlineKeyboard:
    def __init__(self, gif_id: int, lang: dict = lang_ru_inline_buttons):
        self._inline_buttons_gif_edit = [
            InlineKeyboardButton(text=lang['modify_tags'], callback_data=f'modify:{gif_id}'),
            InlineKeyboardButton(text=lang['delete_gif'], callback_data=f'delete:{gif_id}')
        ]

    def keyboard_gif_edit(self):
        return InlineKeyboardMarkup(inline_keyboard=[self._inline_buttons_gif_edit])


class BotReplyKeyboard:
    def __init__(self, lang: dict = lang_ru_inline_buttons):
        self._reply_buttons_main_menu = [
            [
                KeyboardButton(text=lang_ru_reply_buttons['save_gifs']),
                KeyboardButton(text=lang_ru_reply_buttons['find']),
            ],
            [
                KeyboardButton(text=lang_ru_reply_buttons['print_all_gifs']),
                KeyboardButton(text=lang_ru_reply_buttons['print_all_tags']),
            ],
        ]
        self._reply_button_cancel = [[KeyboardButton(text=lang_ru_reply_buttons['cancel'])]]

        self._reply_buttons_gif_saving = [
            [
                KeyboardButton(text=lang_ru_reply_buttons['cancel']),
                KeyboardButton(text=lang_ru_reply_buttons['now_tags']),
            ],
        ]

    def remove(self):
        return ReplyKeyboardRemove()

    def keyboard_main(self):
        return ReplyKeyboardMarkup(
            keyboard=self._reply_buttons_main_menu,
            resize_keyboard=True,
        )

    def keyboard_cancel(self):
        return ReplyKeyboardMarkup(
            keyboard=self._reply_button_cancel,
            resize_keyboard=True,
        )

    def keyboard_gif_saving(self):
        return ReplyKeyboardMarkup(
            keyboard=self._reply_buttons_gif_saving,
            resize_keyboard=True,
        )
