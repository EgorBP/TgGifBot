from aiogram import Bot
from aiogram.types import (
BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,
KeyboardButton, ReplyKeyboardRemove
)

from lexicon import lang_ru_menu, lang_ru_inline_buttons, lang_ru_reply_buttons


class BotMainMenuButton:
    """
    Класс для установки команд бота в главном меню.
    """
    menu_button = [
        BotCommand(command='/start', description=lang_ru_menu['button_start']),
        BotCommand(command='/help', description=lang_ru_menu['button_help'])
    ]

    @staticmethod
    async def set_commands(bot: Bot):
        """
        Установить команды бота для главного меню.

        Args:
            bot (Bot): Экземпляр бота Aiogram.

        Returns:
            None
        """
        await bot.set_my_commands(BotMainMenuButton.menu_button)


class BotInlineKeyboard:
    """
    Класс для создания inline-клавиатуры под GIF.

    Attributes:
        _inline_buttons_gif_edit (list[InlineKeyboardButton]): Список кнопок для редактирования GIF.
    """

    def __init__(self, gif_id: int, lang: dict = lang_ru_inline_buttons):
        """
        Инициализация inline-клавиатуры для конкретного GIF.

        Args:
            gif_id (int): Идентификатор GIF.
            lang (dict): Словарь с текстами кнопок.
        """
        self._inline_buttons_gif_edit = [
            InlineKeyboardButton(text=lang['modify_tags'], callback_data=f'modify:{gif_id}'),
            InlineKeyboardButton(text=lang['delete_gif'], callback_data=f'delete:{gif_id}')
        ]

    def keyboard_gif_edit(self) -> InlineKeyboardMarkup:
        """
        Получить объект InlineKeyboardMarkup для отправки с GIF.

        Returns:
            InlineKeyboardMarkup: Inline-клавиатура.
        """
        return InlineKeyboardMarkup(inline_keyboard=[self._inline_buttons_gif_edit])


class BotReplyKeyboard:
    """
    Класс для создания reply-клавиатур для бота.

    Attributes:
        _reply_buttons_main_menu (list[list[KeyboardButton]]): Кнопки главного меню.
        _reply_button_cancel (list[list[KeyboardButton]]): Кнопка отмены.
        _reply_buttons_gif_saving (list[list[KeyboardButton]]): Кнопки для режима сохранения GIF.
    """

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

    def remove(self) -> ReplyKeyboardRemove:
        """
        Получить объект для удаления клавиатуры.

        Returns:
            ReplyKeyboardRemove: Клавиатура удаления.
        """
        return ReplyKeyboardRemove()

    def keyboard_main(self) -> ReplyKeyboardMarkup:
        """
        Получить reply-клавиатуру главного меню.

        Returns:
            ReplyKeyboardMarkup: Главная клавиатура.
        """
        return ReplyKeyboardMarkup(
            keyboard=self._reply_buttons_main_menu,
            resize_keyboard=True,
        )

    def keyboard_cancel(self) -> ReplyKeyboardMarkup:
        """
        Получить клавиатуру с кнопкой отмены.

        Returns:
            ReplyKeyboardMarkup: Клавиатура отмены.
        """
        return ReplyKeyboardMarkup(
            keyboard=self._reply_button_cancel,
            resize_keyboard=True,
        )

    def keyboard_gif_saving(self) -> ReplyKeyboardMarkup:
        """
        Получить клавиатуру для режима сохранения GIF.

        Returns:
            ReplyKeyboardMarkup: Клавиатура сохранения GIF.
        """
        return ReplyKeyboardMarkup(
            keyboard=self._reply_buttons_gif_saving,
            resize_keyboard=True,
        )
