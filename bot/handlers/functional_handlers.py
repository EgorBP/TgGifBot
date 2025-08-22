from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from bot.lexicon import lang_ru
from bot.states import FSMGifRegister
from bot.services import update_user_gif_tags
from bot.keyboards import BotReplyKeyboard
from bot.utils import execute_tags_from_message


router = Router()
reply_keyboard = BotReplyKeyboard()


@router.message(F.animation, StateFilter(default_state))
async def gif_answer(msg: Message, state: FSMContext):
    """
    Обработчик получения GIF от пользователя.

    Сохраняет file_id гифки в FSMContext и переводит состояние
    в ожидание ввода тегов, отправляя сообщение с инструкцией.
    """
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
    """
    Обработчик для неверного типа сообщения при вводе тегов.

    Сообщение должно быть текстовым; если нет, уведомляет пользователя.
    """
    await message.answer(lang_ru['only_text'])


@router.message(StateFilter(FSMGifRegister.gif_tags))
async def add_tags_to_gif(message: Message, state: FSMContext):
    """
    Обработчик добавления тегов к GIF.

    Извлекает теги из текста, сохраняет их в FSMContext, отправляет
    запрос на сервер для обновления тегов GIF и информирует пользователя о результате.
    """
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
