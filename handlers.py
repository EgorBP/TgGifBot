import os, json
from time import time

from aiogram import Router, F
from aiogram.types import message, FSInputFile
from aiogram.filters import Command

from lexicon import lang_ru


router = Router()
last_message = False

@router.message(Command('start'))
async def start_command_answer(msg):
    await msg.answer(lang_ru['/start'])


@router.message(F.animation)
async def gif_answer(msg):
    global last_message

    bot = msg.bot

    gif_id = msg.animation.file_id      # Получаем id гифки
    gif = await bot.get_file(gif_id)    # Получаем сам файл гифки(там есть id, и др хуй знает зачем)

    folder_path = 'animations'
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{gif_id}.mp4")  # Путь куда сохранить гифку

    if not os.path.exists(file_path):
        await bot.download(gif, destination=file_path)      # Скачивает, если пути нету создает его

    await msg.answer(text=lang_ru['gif_tag'])
    last_message = True


@router.message(lambda msg: last_message)
async def add_tags_to_gif(msg):
    directory = 'animations'
    # Получаем список всех файлов в директории
    files = os.listdir(directory)
    # Получаем полный путь к каждому файлу в директории
    full_paths = [os.path.join(directory, file) for file in files]
    # Отсортируем файлы по времени создания (по убыванию)
    latest_file = max(full_paths, key=os.path.getctime)
    latest_file_name = os.path.basename(latest_file)

    to_json = {latest_file_name: msg.text.replace(' ', '').split(',')}

    with open('attributes.json', 'r+') as file:
        if os.stat('attributes.json').st_size:
            all_gifs = json.load(file)
        else:
            all_gifs = {}
        file.seek(0)

        all_gifs.update(to_json)
        json.dump(all_gifs, file, indent=4, ensure_ascii=False)

    await msg.answer(text=lang_ru['successfully_saved'])

    global last_message
    last_message = False


@router.message(Command('take_all'))
async def send_all_gifs(msg):
    with open('attributes.json', 'r') as file:
        if os.stat('attributes.json').st_size:
            all_gifs = json.load(file)
        else:
            all_gifs = {}

    for gif in os.listdir('animations'):
        file_path = os.path.join('animations', gif)
        gif_to_send = FSInputFile(file_path)

        await msg.answer_animation(gif_to_send)
        await msg.answer(f"Теги: {', '.join(all_gifs[gif])}")

