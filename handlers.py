import os
from time import time

from aiogram import Router, F
from aiogram.types import message, FSInputFile
from aiogram.filters import Command

from lexicon import lang_ru


router = Router()

@router.message(Command('start'))
async def start_command_answer(msg):
    await msg.answer(lang_ru['/start'])


@router.message(F.animation)
async def gif_answer(msg):
    st_time = time()
    bot = msg.bot

    gif_id = msg.animation.file_id      # Получаем id гифки
    gif = await bot.get_file(gif_id)    # Получаем сам файл гифки(там есть id, и др хуй знает зачем)

    folder_path = 'animations'
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{gif_id}.mp4")  # Путь куда сохранить гифку,
                                                            # (.join ставит '/' или '\' для винды или линукса)
    if not os.path.exists(file_path):
        await bot.download(gif, destination=file_path)      # Скачивает, если пути нету создает

    print(time() - st_time)


@router.message(Command('take_all'))
async def send_all_gifs(msg):
    for gif in os.listdir('animations'):
        file_path = os.path.join('animations', gif)
        gif_to_send = FSInputFile(file_path)

        await msg.answer_animation(gif_to_send)


