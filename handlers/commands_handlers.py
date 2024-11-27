import json

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon import lang_ru
from states import FSMGifRegister


router = Router()


@router.message(Command('start'))
async def start_command_answer(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(lang_ru['/start'])

from aiogram.fsm.state import default_state

@router.message(Command('take_all'), StateFilter(default_state))
async def send_all_gifs(message: Message):
    with open('attributes.json', 'r') as file:
        if os.stat('attributes.json').st_size:
            all_gifs = json.load(file)
        else:
            all_gifs = {}

    for gif in os.listdir('animations'):
        file_path = os.path.join('animations', gif)
        gif_to_send = FSInputFile(file_path)

        await message.answer_animation(gif_to_send)
        await message.answer(f"Теги: {', '.join(all_gifs[gif])}")
        # gif_id = list(all_gifs.keys())[0]
        # gif_id = gif_id[:gif_id.find('.')]
        # await msg.answer_animation(gif_id)


