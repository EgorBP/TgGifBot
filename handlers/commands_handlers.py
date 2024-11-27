import json
import os

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


@router.message(Command('cancel'), StateFilter(FSMGifRegister.gif_tag))
async def stop_adding(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(lang_ru['canceled'])


@router.message(Command('send_gifs'), ~StateFilter(default_state))
async def not_now_sending(message: Message):
    await message.answer(lang_ru['not_now'])


@router.message(Command('send_gifs'), StateFilter(default_state))
async def send_all_gifs(message: Message):
    path = os.path.join('data', 'data.json')
    user_id = str(message.from_user.id)

    with open(path, 'r') as file:
        try:
            data = json.load(file)
            gifs_data = data[user_id]['gifs_data']
        except (json.JSONDecodeError, KeyError):
            await message.answer(lang_ru['no_gifs'])
            return

    for gif_name in gifs_data.keys():
        gif_id = gifs_data[gif_name]['gif_id']
        gif_tags = ', #'.join(gifs_data[gif_name]['gif_tags'])

        await message.answer_animation(
            gif_id,
            caption=f'<b>Теги </b>:  #{gif_tags}',
        )
