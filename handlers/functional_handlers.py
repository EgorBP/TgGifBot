from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon import lang_ru, lang_ru_reply_buttons
from states import FSMGifRegister
from services import update_json_by_new_gif


router = Router()


@router.message(F.animation, StateFilter(default_state))
async def gif_answer(msg: Message, state: FSMContext):
    await state.set_state(FSMGifRegister.gif_id)

    gif_id = msg.animation.file_id      # Получаем id гифки

    await state.update_data(gif_id=gif_id)

    await msg.answer(text=lang_ru['now_send_tags'])
    await state.set_state(FSMGifRegister.gif_tag)


@router.message(StateFilter(FSMGifRegister.gif_tag), ~F.text)
async def add_tags_to_gif(message: Message):
    await message.answer(lang_ru['only_text'])


@router.message(StateFilter(FSMGifRegister.gif_tag))
async def add_tags_to_gif(message: Message, state: FSMContext):
    tags: list[str] = message.text.replace('#', '').split(',')
    tags: list[str] = [f'#{tag.strip()}' for tag in tags]
    await state.update_data(gif_tag=tags)

    data = await state.get_data()               # In json int was always
    user_id = str(message.from_user.id)         # convert to string

    update_json_by_new_gif(user_id, data)

    await message.answer(text=lang_ru['successfully_saved'])
    await state.clear()


@router.message()
async def bad_message(message: Message):
    await message.answer(lang_ru['wrong_message'])