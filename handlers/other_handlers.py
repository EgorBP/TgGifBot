from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from lexicon import lang_ru


router = Router()


@router.message(Command('github'))
async def github(message: Message):
    await message.answer(lang_ru['github'])


@router.message()
async def bad_message(message: Message):
    await message.answer(lang_ru['wrong_message'])