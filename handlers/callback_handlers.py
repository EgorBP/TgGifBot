from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboards import BotInlineKeyboard, BotReplyKeyboard
from services import update_user_gif_tags, search_user_gifs
from lexicon import lang_ru
from states import FSMUpdatingTags


router = Router()
reply_keyboard = BotReplyKeyboard()


@router.callback_query(F.data.split(':')[0] == 'delete')
async def callback_deleting(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    gif_name = callback.data.split(':')[1]

    data = load_all_data(callback.message)

    try:
        del data[user_id]['gifs_data'][gif_name]
    except KeyError:
        await callback.message.edit_caption(
            caption=lang_ru['deleted_later']
        )
        return

    update_json(data)

    await callback.message.edit_caption(
        caption=lang_ru['deleted_gif']
    )


@router.callback_query(F.data.split(':')[0] == 'modify', StateFilter(default_state))
async def callback_modifying_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(caption=f'➡️{callback.message.caption}⬅️\n'
                                                f'{lang_ru["now_edit"]}')

    await state.set_state(FSMUpdatingTags.updating)
    await state.update_data(
        updating=[callback.message.message_id, callback.message.caption, callback.data.split(':')[1]]
    )

    await callback.message.answer(
        text=lang_ru['send_new_gifs'],
        reply_markup=reply_keyboard.keyboard_cancel(),
    )


@router.message(~F.text, StateFilter(FSMUpdatingTags.updating))
async def wrong_msg(message: Message):
    await message.answer(lang_ru['only_text'])


@router.message(StateFilter(FSMUpdatingTags.updating))
async def modifying_tags(message: Message, state: FSMContext):
    data = load_all_data(message)
    gif_name = (await state.get_data())['updating'][2]
    user_id = str(message.from_user.id)
    bot = message.bot
    caption_data = (await state.get_data())['updating']
    inline_keyboard = BotInlineKeyboard(caption_data[2])

    new_tags: list[str] = message.text.replace('#', '').split(',')
    new_tags: list[str] = [f'#{tag.strip().lower()}' for tag in new_tags]

    data[user_id]['gifs_data'][gif_name]['gif_tags'] = new_tags

    update_json(data)

    await state.clear()
    await bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=caption_data[0],
        caption=caption_data[1],
        reply_markup=inline_keyboard.keyboard_gif_edit(),
    )
    await message.answer(
        text=lang_ru['new_tags'],
        reply_markup=reply_keyboard.keyboard_main(),
    )