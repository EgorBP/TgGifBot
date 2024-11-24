import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, ContentType, File

from lexicon import lang_ru

BOT_TOKEN = '6125202965:AAEmJ7Pv5Znr71GwcPuzWPPXk8IK89ZFEuw'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_command_answer(message):
    await message.answer(lang_ru['hi'])

@dp.message(F.animation)
async def gif_answer(message):
    gif_id = message.animation.file_id  # Получаем id гифки
    gif = await bot.get_file(gif_id)    # Получаем сам файл гифки(там есть id, и др хуй знает зачем)
    folder_path = 'animations'
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{gif_id}.mp4")  # Путь куда сохранить гифку,
    await bot.download(gif, destination=file_path)          # (.join ставит '/' или '\' для винды или линукса)

    gif_to_send = FSInputFile(file_path)
    await message.answer_animation(gif_to_send)


if __name__ == '__main__':
    dp.run_polling(bot)