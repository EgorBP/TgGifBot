from aiogram import Bot
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import MenuButtonType

from lexicon import lang_ru_menu, lang_ru_inline_buttons


class BotMainMenuButton:
    menu_button = [
        BotCommand(command='/start', description=lang_ru_menu['button_start']),
        BotCommand(command='/help', description=lang_ru_menu['button_help'])
    ]

    @staticmethod
    async def set_commands(bot: Bot):
        await bot.set_my_commands(BotMainMenuButton.menu_button)


class BotInlineKeyboard:
    def __init__(self, gif_name: str, lang: dict = lang_ru_inline_buttons):
        self.inline_buttons_gif_edit = [
            InlineKeyboardButton(text=lang['modify_tags'], callback_data=f'modify:{gif_name}'),
            InlineKeyboardButton(text=lang['delete_gif'], callback_data=f'delete:{gif_name}')
        ]

    def set_keyboard_gif_edit(self):
        return InlineKeyboardMarkup(inline_keyboard=[self.inline_buttons_gif_edit])