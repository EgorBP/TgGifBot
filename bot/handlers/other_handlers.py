from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.lexicon import lang_ru


router = Router()


@router.message(Command('github'))
async def github(message: Message):
    """
    Обработчик команды /github.

    Отправляет пользователю ссылку на GitHub проекта или соответствующее сообщение.
    """
    await message.answer(lang_ru['github'])


@router.message()
async def bad_message(message: Message):
    """
    Обработчик всех остальных сообщений, не соответствующих командам.

    Уведомляет пользователя о неверном формате или неподдерживаемом сообщении.
    """
    await message.answer(lang_ru['wrong_message'])