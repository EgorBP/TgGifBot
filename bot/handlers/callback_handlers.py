from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.keyboards import BotInlineKeyboard, BotReplyKeyboard
from bot.services import update_user_gif_tags, delete_user_gif
from bot.lexicon import lang_ru
from bot.states import FSMUpdatingTags
from bot.utils import prepare_tags_to_send, execute_tags_from_message


router = Router()
reply_keyboard = BotReplyKeyboard()


@router.callback_query(F.data.split(':')[0] == 'delete')
async def callback_deleting(callback: CallbackQuery):
    """
    Обработчик нажатия кнопки удаления GIF.

    Удаляет GIF пользователя на сервере и обновляет подпись сообщения
    в зависимости от результата операции.
    """
    user_id = callback.from_user.id
    db_gif_id = int(callback.data.split(':')[1])

    response = await delete_user_gif(user_id, db_gif_id)

    if response.code != 200:
        await callback.message.edit_caption(
            caption=lang_ru['deleted_later']
        )
        return

    await callback.message.edit_caption(
        caption=lang_ru['deleted_gif']
    )


@router.callback_query(F.data.split(':')[0] == 'modify', StateFilter(default_state))
async def callback_modifying_start(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик начала редактирования тегов GIF.

    Изменяет подпись сообщения, сохраняет состояние FSM с данными GIF
    и уведомляет пользователя о возможности отправки новых тегов.
    """
    await callback.message.edit_caption(caption=f'➡️{callback.message.caption}⬅️\n'
                                                f'{lang_ru["now_edit"]}')

    await state.set_state(FSMUpdatingTags.updating)
    await state.update_data(
        updating=[
            callback.message.message_id,
            callback.message.caption,
            callback.message.animation.file_id,
            int(callback.data.split(':')[1])
        ]
    )

    await callback.message.answer(
        text=lang_ru['send_new_gifs'],
        reply_markup=reply_keyboard.keyboard_cancel(),
    )


@router.message(~F.text, StateFilter(FSMUpdatingTags.updating))
async def wrong_msg(message: Message):
    """
    Обработка неверного типа сообщения при редактировании тегов GIF.

    Сообщение должно быть текстовым.
    """
    await message.answer(lang_ru['only_text'])


@router.message(StateFilter(FSMUpdatingTags.updating))
async def modifying_tags(message: Message, state: FSMContext):
    """
    Обновление тегов существующего GIF.

    Извлекает новые теги из текста, отправляет запрос на сервер для обновления,
    редактирует подпись исходного сообщения и уведомляет пользователя о результате.
    """
    data = await state.get_data()
    tg_gif_id = data['updating'][2]
    tg_user_id = message.from_user.id
    bot = message.bot
    caption_data = data['updating']
    inline_keyboard = BotInlineKeyboard(data['updating'][3])

    new_tags: list[str] = execute_tags_from_message(message.text)

    response = await update_user_gif_tags(tg_user_id, tg_gif_id, new_tags)
    if response.code != 200:
        await message.answer(
            text=lang_ru['error'],
            reply_markup=reply_keyboard.keyboard_main(),
        )
        await state.clear()
        return

    await state.clear()
    await bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=caption_data[0],
        caption=f'<b>Новые теги:</b>  {prepare_tags_to_send(new_tags)}',
        reply_markup=inline_keyboard.keyboard_gif_edit(),
    )
    await message.answer(
        text=lang_ru['new_tags'],
        reply_markup=reply_keyboard.keyboard_main(),
    )