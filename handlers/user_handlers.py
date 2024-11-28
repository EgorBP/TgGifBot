import json
import os

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon import lang_ru
from states import FSMGifRegister
from services import load_gifs_data, get_all_tags


router = Router()


@router.message(Command('start'))
async def start_command_answer(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(lang_ru['/start'])


@router.message(Command('cancel'), StateFilter(FSMGifRegister.gif_tag))
async def stop_adding(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(lang_ru['cancel_process'])


@router.message(Command('send_gifs'), ~StateFilter(default_state))
async def not_now_sending(message: Message):
    await message.answer(lang_ru['not_now'])


@router.message(Command('send_gifs'), StateFilter(default_state))
async def send_all_gifs(message: Message):
    user_id = str(message.from_user.id)

    gifs_data = load_gifs_data(user_id)
    if gifs_data is None:
        await message.answer(lang_ru['no_gifs'])
        return

    for gif_name in gifs_data.keys():
        gif_id = gifs_data[gif_name]['gif_id']
        gif_tags = ', '.join(gifs_data[gif_name]['gif_tags'])

        await message.answer_animation(
            gif_id,
            caption=f'<b>Теги </b>:  {gif_tags}',
        )


@router.message(Command('send_tags'), StateFilter(default_state))
async def send_all_tags(message: Message):
    user_id = str(message.from_user.id)

    all_tags = get_all_tags(user_id)
    if all_tags is None:
        await message.answer(lang_ru['no_gifs'])
        return

    await message.answer(f'<b>Все теги</b>:  {all_tags}')


@router.message(Command('find'), StateFilter(default_state))
async def finding_gif_by_tags(message: Message, state: FSMContext):
    pass
