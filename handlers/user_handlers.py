import json
import os

from aiogram import Router, F
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon import lang_ru, lang_ru_reply_buttons
from states import FSMGifRegister, FSMFindingGif, FSMUpdatingTags
from services import load_gifs_data, get_all_tags_separated
from keyboards import BotMainMenuButton, BotInlineKeyboard, BotReplyKeyboard


router = Router()
reply_keyboard = BotReplyKeyboard()


@router.message(Command('start'))
async def start_command_answer(message: Message, state: FSMContext):
    await BotMainMenuButton.set_commands(message.bot)
    await state.clear()
    await message.answer(
        text=lang_ru['/start'],
        reply_markup=reply_keyboard.keyboard_main(),
    )



@router.message(Command('help'), StateFilter(default_state))
async def help_command_answer(message: Message):
    await message.answer(lang_ru['/help'])


@router.message(
    or_f(Command('cancel'), F.text.startswith(lang_ru_reply_buttons['cancel'])),
    StateFilter(FSMUpdatingTags.updating)
)
async def stop_updating_tags(message: Message, state: FSMContext):
    caption_data = (await state.get_data())['updating']
    bot = message.bot
    inline_keyboard = BotInlineKeyboard(caption_data[2])

    await bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=caption_data[0],
        caption=caption_data[1],
        reply_markup=inline_keyboard.keyboard_gif_edit(),
    )

    await state.clear()
    await message.answer(
        text=lang_ru['cancel_process'],
        reply_markup=reply_keyboard.keyboard_main(),
    )


@router.message(
    or_f(Command('cancel'), F.text.startswith(lang_ru_reply_buttons['cancel'])),
    ~StateFilter(default_state)
)
async def stop_adding(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=lang_ru['cancel_process'],
        reply_markup=reply_keyboard.keyboard_main(),
    )


@router.message(Command('send_gifs'), ~StateFilter(default_state))
async def not_now_sending(message: Message):
    await message.answer(lang_ru['not_now'])


@router.message(
    or_f(Command('send_gifs'), F.text.startswith(lang_ru_reply_buttons['print_all_gifs'])),
    StateFilter(default_state)
)
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
            reply_markup=inline_markup.keyboard_gif_edit(),
        )


@router.message(
    or_f(Command('send_tags'), F.text.startswith(lang_ru_reply_buttons['print_all_tags'])),
    StateFilter(default_state)
)
async def send_all_tags(message: Message):
    all_tags = get_all_tags_separated(message)
    if all_tags is None or all_tags == '':
        await message.answer(lang_ru['no_gifs_or_tags'])
        return

    await message.answer(f'<b>Все теги:</b>  {all_tags}')


@router.message(
    or_f(Command('find'), F.text.startswith(lang_ru_reply_buttons['find'])),
    StateFilter(default_state)
)
async def start_finding_gif_by_tags(message: Message, state: FSMContext):
    all_tags = get_all_tags_separated(message)
    if all_tags is None or all_tags == '':
        await message.answer(lang_ru['no_gifs'])
        return

    await message.answer(
        text=f'{lang_ru['start_finding']}\n'
        f'<b>Доступные теги:</b>  {all_tags}',
        reply_markup=reply_keyboard.keyboard_cancel(),
    )

    await state.set_state(FSMFindingGif.find)


@router.message(StateFilter(FSMFindingGif.find), ~F.text)
async def send_gif_by_tags_wrong_message(message: Message):
    await message.answer(lang_ru['need_text'])


@router.message(StateFilter(FSMFindingGif.find), F.text)
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
                reply_markup=inline_markup.keyboard_gif_edit(),
            )

    await state.clear()
