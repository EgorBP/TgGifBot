import inspect

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, ContentType

from lexicon import lang_ru


bot = Bot(token='6125202965:AAEmJ7Pv5Znr71GwcPuzWPPXk8IK89ZFEuw')
dp = Dispatcher()


@dp.message(Command('start'))
async def start_command_answer(message):
    await message.answer(lang_ru['hi'])

@dp.message(F.photo)
async def photo_answer(message):
    await message.answer_photo(photo=message.photo[-1].file_id)

@dp.message(F.document)
async def compressed_photo_answer(message):
    await message.answer_document(document=message.document.file_id)


if __name__ == '__main__':
    dp.run_polling(bot)