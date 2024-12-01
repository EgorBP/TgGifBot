from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, InputMediaAnimation
from aiogram.filters import StateFilter

from keyboards import BotInlineKeyboard, BotReplyKeyboard
from services import load_all_data, update_json_by_deleting_gif
from lexicon import lang_ru, lang_ru_reply_buttons
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

    update_json_by_deleting_gif(data)

    await callback.message.edit_caption(
        caption=lang_ru['deleted_gif']
    )


@router.callback_query(F.data.split(':')[0] == 'modify', StateFilter(default_state))
async def callback_modifying_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(caption=f'➡️{callback.message.caption}⬅️\n'
                                                f'{lang_ru['now_edit']}')

    await state.set_state(FSMUpdatingTags.updating)
    await state.update_data(updating=callback.callback.message.caption)

    await callback.message.answer(
        text=lang_ru['send_new_gifs'],
        reply_markup=reply_keyboard.keyboard_cancel(),
    )

