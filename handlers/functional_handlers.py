from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon import lang_ru
from states import FSMGifRegister
from services import update_json


router = Router()


@router.message(F.animation, StateFilter(default_state))
async def gif_answer(msg: Message, state: FSMContext):
    gif_id = msg.animation.file_id      # Получаем id гифки

    await state.update_data(gif_id=gif_id)

    await msg.answer(text=lang_ru['gif_saved'])
    await state.set_state(FSMGifRegister.gif_tag)


@router.message(StateFilter(FSMGifRegister.gif_tag))
async def add_tags_to_gif(message: Message, state: FSMContext):
    tags = message.text.split(',')
    tags: list[str] = [tag.strip() for tag in tags]
    await state.update_data(gif_tag=tags)

    data = await state.get_data()               # In json int was always
    user_id = str(message.from_user.id)         # convert to string

    update_json(user_id, data)

    await message.answer(text=lang_ru['successfully_saved'])
    await state.clear()

