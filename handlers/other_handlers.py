from aiogram import Router
from aiogram.types import Message

from lexicon import lang_ru


router = Router()


@router.message()
async def bad_message(message: Message):
    await message.answer(lang_ru['wrong_message'])