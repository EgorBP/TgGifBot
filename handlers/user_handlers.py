from aiogram import Router, F
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon import lang_ru, lang_ru_reply_buttons
from states import FSMFindingGif, FSMUpdatingTags, FSMGifSaving
from services import update_user_gif_tags, search_user_gifs, get_all_user_tags, send_gif_with_inline_keyboard
from keyboards import BotMainMenuButton, BotInlineKeyboard, BotReplyKeyboard
from utils import prepare_tags_to_send, execute_tags_from_message
import asyncio


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
    StateFilter(FSMUpdatingTags.updating),
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
    ~StateFilter(default_state),
)
async def stop_adding(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=lang_ru['cancel_process'],
        reply_markup=reply_keyboard.keyboard_main(),
    )


@router.message(
    or_f(Command('save_gifs'), F.text.startswith(lang_ru_reply_buttons['save_gifs'])),
    StateFilter(default_state),
)
async def start_gifs_saving(message: Message, state: FSMContext):
    await message.answer(
        text=lang_ru['send'],
        reply_markup=reply_keyboard.keyboard_gif_saving(),
    )

    await state.set_state(FSMGifSaving.gifs_id)


@router.message(
    F.animation,
    StateFilter(FSMGifSaving.gifs_id),
)
async def gifs_saving(message: Message, state: FSMContext):
    try:
        gifs_id = (await state.get_data())['gifs_id']
    except KeyError:
        gifs_id = []

    gifs_id.append(message.animation.file_id)

    await state.update_data(gifs_id=gifs_id)


@router.message(
    F.text == lang_ru_reply_buttons['now_tags'],
    StateFilter(FSMGifSaving.gifs_id),
)
async def start_tags_gifs_saving(message: Message, state: FSMContext):
    try:
        # check = (await state.get_data())['gifs_id']
        await state.set_state(FSMGifSaving.gifs_tags)
        await message.answer(
            text=lang_ru['now_tags'],
            reply_markup=reply_keyboard.keyboard_cancel(),
        )
    except KeyError:
        await message.answer(
            text=lang_ru['no_gifs_to_one_tags'],
            reply_markup=reply_keyboard.keyboard_main(),
        )

@router.message(
    ~F.text,
    StateFilter(FSMGifSaving.gifs_tags),
)
async def tags_gifs_saving_bad_message(message: Message):
    await message.answer(lang_ru['only_text'])


@router.message(
    F.text,
    StateFilter(FSMGifSaving.gifs_tags),
)
async def tags_gifs_saving(message: Message, state: FSMContext):
    gifs_tags: list[str] = execute_tags_from_message(message.text)
    await state.update_data(gifs_tags=gifs_tags)

    gifs_data = await state.get_data()
    user_id = message.from_user.id

    tasks = [update_user_gif_tags(user_id, gif_id, gifs_tags) for gif_id in gifs_data['gifs_id']]
    task_responses = await asyncio.gather(*tasks)

    for response in task_responses:
        if response.code != 200:
            await message.answer(
                text=lang_ru['partly_saved'],
                reply_markup=reply_keyboard.keyboard_main(),
            )
            await state.clear()
            return

    await message.answer(
        text=lang_ru['successfully_saved'],
        reply_markup=reply_keyboard.keyboard_main(),
    )
    await state.clear()


@router.message(
    or_f(Command('send_gifs'), F.text.startswith(lang_ru_reply_buttons['print_all_gifs'])),
    ~StateFilter(default_state),
)
async def not_now_sending(message: Message):
    await message.answer(lang_ru['not_now'])


@router.message(
    or_f(Command('send_gifs'), F.text.startswith(lang_ru_reply_buttons['print_all_gifs'])),
    StateFilter(default_state),
)
async def send_all_gifs(message: Message):
    response = await search_user_gifs(message.from_user.id)

    if response.code != 200:
        await message.answer(
            text=lang_ru['no_gifs'],
            reply_markup=reply_keyboard.keyboard_main(),
        )
        return

    data = response.data

    if not data['gifs_data']:
        await message.answer(
            text=lang_ru['nothing_founded'],
            reply_markup=reply_keyboard.keyboard_main(),
        )
        return

    tasks = []
    for gif_data in data['gifs_data']:
        inline_markup = BotInlineKeyboard(gif_data['id'])
        tags = prepare_tags_to_send(gif_data['tags'])
        tasks.append(send_gif_with_inline_keyboard(message, gif_data['tg_gif_id'], tags, inline_markup))
    await asyncio.gather(*tasks)


@router.message(
    or_f(Command('send_tags'), F.text.startswith(lang_ru_reply_buttons['print_all_tags'])),
    ~StateFilter(default_state),
)
async def not_now_sending(message: Message):
    await message.answer(lang_ru['not_now'])


@router.message(
    or_f(Command('send_tags'), F.text.startswith(lang_ru_reply_buttons['print_all_tags'])),
    StateFilter(default_state),
)
async def send_all_tags(message: Message):
    response = await get_all_user_tags(message.from_user.id)

    if response.code == 200:
        all_tags = prepare_tags_to_send(response.data)
    else:
        await message.answer(lang_ru['no_gifs_or_tags'])
        return

    await message.answer(f'<b>Все теги:</b>  {all_tags}')


@router.message(
    or_f(Command('find'), F.text.startswith(lang_ru_reply_buttons['find'])),
    StateFilter(default_state),
)
async def start_finding_gif_by_tags(message: Message, state: FSMContext):
    response = await get_all_user_tags(message.from_user.id)

    if response.code == 200:
        all_tags = prepare_tags_to_send(response.data)
    else:
        await message.answer(lang_ru['no_gifs_or_tags'])
        return

    await message.answer(
        text=f'{lang_ru["start_finding"]}\n\n'
        f'<b>Доступные теги:</b>  {all_tags}',
        reply_markup=reply_keyboard.keyboard_cancel(),
    )

    await state.set_state(FSMFindingGif.find)


@router.message(StateFilter(FSMFindingGif.find), ~F.text)
async def send_gif_by_tags_wrong_message(message: Message):
    await message.answer(lang_ru['need_text'])


@router.message(StateFilter(FSMFindingGif.find), F.text)
async def send_gif_by_tags(message: Message, state: FSMContext):
    tags_to_find: list[str] = execute_tags_from_message(message.text)

    response = await search_user_gifs(message.from_user.id, tags_to_find)

    if response.code != 200:
        await message.answer(
            text=lang_ru['no_gifs'],
            reply_markup=reply_keyboard.keyboard_main(),
        )
        await state.clear()
        return

    data = response.data

    if not data['gifs_data']:
        await message.answer(
            text=lang_ru['nothing_founded'],
            reply_markup=reply_keyboard.keyboard_main(),
        )
        await state.clear()
        return

    tasks = []
    for gif_data in data['gifs_data']:
        inline_markup = BotInlineKeyboard(gif_data['id'])
        tags = prepare_tags_to_send(gif_data['tags'])
        tasks.append(send_gif_with_inline_keyboard(message, gif_data['tg_gif_id'], tags, inline_markup))
    await asyncio.gather(*tasks)

    await message.answer(
        text=lang_ru['all'],
        reply_markup=reply_keyboard.keyboard_main(),
    )
    await state.clear()
