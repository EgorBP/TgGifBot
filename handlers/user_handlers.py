import json
import os

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon import lang_ru
from states import FSMGifRegister, FSMOtherStates
from services import load_gifs_data, get_all_tags, get_all_tags_separated
from keyboards import BotInlineKeyboard


router = Router()


@router.message(Command('start'))
async def start_command_answer(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(lang_ru['/start'])


@router.message(Command('help'), StateFilter(default_state))
async def help_command_answer(message: Message):
    await message.answer(lang_ru['/help'])


@router.message(Command('cancel'), ~StateFilter(default_state))
async def stop_adding(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(lang_ru['cancel_process'])


@router.message(Command('send_gifs'), ~StateFilter(default_state))
async def not_now_sending(message: Message):
    await message.answer(lang_ru['not_now'])


@router.message(Command('send_gifs'), StateFilter(default_state))
async def send_all_gifs(message: Message):
    gifs_data = load_gifs_data(message)
    if gifs_data is None or gifs_data == {}:
        await message.answer(lang_ru['no_gifs'])
        return

    for gif_name in gifs_data.keys():
        gif_id = gifs_data[gif_name]['gif_id']
        gif_tags = ', '.join(gifs_data[gif_name]['gif_tags'])
        inline_markup = BotInlineKeyboard(gif_name)

        await message.answer_animation(
            gif_id,
            caption=f'<b>Теги:</b>  {gif_tags}',
            reply_markup=inline_markup.set_keyboard_gif_edit()
        )


@router.message(Command('send_tags'), StateFilter(default_state))
async def send_all_tags(message: Message):
    all_tags = get_all_tags(message)
    if all_tags is None or all_tags == {}:
        await message.answer(lang_ru['no_gifs_or_tags'])
        return

    await message.answer(f'<b>Все теги:</b>  {all_tags}')


@router.message(Command('find'), StateFilter(default_state))
async def start_finding_gif_by_tags(message: Message, state: FSMContext):
    all_tags = get_all_tags_separated(message)
    if all_tags is None or all_tags == {}:
        await message.answer(lang_ru['no_gifs'])
        return

    await message.answer(text=f'{lang_ru['start_finding']}\n'
                              f'<b>Доступные теги:</b>  {all_tags}')

    await state.set_state(FSMOtherStates.find)


@router.message(StateFilter(FSMOtherStates.find), ~F.text)
async def send_gif_by_tags_wrong_message(message: Message):
    await message.answer(lang_ru['need_text'])


@router.message(StateFilter(FSMOtherStates.find), F.text)
async def send_gif_by_tags(message: Message, state: FSMContext):
    gifs_data = load_gifs_data(message)
    if gifs_data is None or gifs_data == {}:
        await message.answer(lang_ru['no_gifs'])
        return

    tags_to_find: list[str] = message.text.replace('#', '').split(',')
    tags_to_find: set[str] = set([f'#{tag.strip()}' for tag in tags_to_find])

    for gif_name in gifs_data.keys():
        gif_id = gifs_data[gif_name]['gif_id']
        gif_tags = set(gifs_data[gif_name]['gif_tags'])
        inline_markup = BotInlineKeyboard(gif_id)

        if tags_to_find.issubset(gif_tags):
            await message.answer_animation(
                gif_id,
                caption=f'<b>Теги:</b>  {', '.join(gif_tags)}',
                reply_markup=inline_markup.set_keyboard_gif_edit()
            )

    await state.clear()
