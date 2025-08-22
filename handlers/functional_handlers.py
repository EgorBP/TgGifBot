from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon import lang_ru
from states import FSMGifRegister
from services import update_user_gif_tags
from keyboards import BotReplyKeyboard
from utils import execute_tags_from_message


router = Router()
reply_keyboard = BotReplyKeyboard()


@router.message(F.animation, StateFilter(default_state))
async def gif_answer(msg: Message, state: FSMContext):
    await state.set_state(FSMGifRegister.gif_id)

    gif_id = msg.animation.file_id      # Получаем id гифки

    await state.update_data(gif_id=gif_id)

    await msg.answer(
        text=lang_ru['now_send_tags'],
        reply_markup=reply_keyboard.keyboard_cancel(),
    )
    await state.set_state(FSMGifRegister.gif_tags)


@router.message(StateFilter(FSMGifRegister.gif_tags), ~F.text)
async def add_tags_to_gif_bad_message(message: Message):
    await message.answer(lang_ru['only_text'])


@router.message(StateFilter(FSMGifRegister.gif_tags))
async def add_tags_to_gif(message: Message, state: FSMContext):
    tags: list[str] = execute_tags_from_message(message.text)
    await state.update_data(gif_tags=tags)

    data = await state.get_data()

    gif_id = data['gif_id']
    gif_tags = data['gif_tags']
    user_id = message.from_user.id

    response = await update_user_gif_tags(user_id, gif_id, gif_tags)

    if response.code == 200:
        await message.answer(
            text=lang_ru['successfully_saved'],
            reply_markup=reply_keyboard.keyboard_main(),
        )
    else:
        await message.answer(
            text=lang_ru['error'],
            reply_markup=reply_keyboard.keyboard_main(),
        )

    await state.clear()
