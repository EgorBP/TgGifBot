from aiogram import Bot
from aiogram.types import MenuButtonCommands, BotCommand
from aiogram.enums import MenuButtonType

from lexicon import lang_ru_menu

class MainMenuButton:
    menu_button = [
        BotCommand(command='/start', description=lang_ru_menu['button_start']),
        BotCommand(command='/help', description=lang_ru_menu['button_help'])
    ]

    @staticmethod
    async def set_commands(bot: Bot):
        await bot.set_my_commands(MainMenuButton.menu_button)