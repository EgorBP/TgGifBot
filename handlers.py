import json
import os

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import FSInputFile

from lexicon import lang_ru
from states import FSMGifRegister

router = Router()


@router.message(Command('start'))
async def start_command_answer(msg):
    # !!!!
    await state.clear()
    await msg.answer(lang_ru['/start'])


@router.message(F.animation, StateFilter(default_state))
async def gif_answer(msg, state):
    bot = msg.bot

    gif_id = msg.animation.file_id      # Получаем id гифки
    gif = await bot.get_file(gif_id)    # Получаем сам файл гифки(там есть id, и др хуй знает зачем)

    folder_path = 'animations'
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{gif_id}.mp4")  # Путь куда сохранить гифку

    if not os.path.exists(file_path):                       # Проверяет скачан ли уже файл
        await bot.download(gif, destination=file_path)      # Скачивает, если пути нету создает его

    await msg.answer(text=lang_ru['gif_saved'])
    await state.update_data(gif_id=gif_id)
    await state.set_state(FSMGifRegister.gif_tag)


@router.message(StateFilter(FSMGifRegister.gif_id))
async def add_tags_to_gif(msg, state):
    latest_file_id = state.get_data()['gif_id']

    tags = [tag.strip().lower() for tag in msg.text.split(',')]
    to_json = {latest_file_id: tags}

    with open('attributes.json', 'r+') as file:
        if os.stat('attributes.json').st_size:
            all_gifs = json.load(file)
        else:
            all_gifs = {}
        file.seek(0)
        file.truncate()

        all_gifs.update(to_json)
        json.dump(all_gifs, file, indent=4, ensure_ascii=False)

    await msg.answer(text=lang_ru['successfully_saved'])
    await state.clear()


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
        # gif_id = list(all_gifs.keys())[0]
        # gif_id = gif_id[:gif_id.find('.')]
        # await msg.answer_animation(gif_id)

