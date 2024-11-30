from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaAnimation

from keyboards import BotInlineKeyboard
from services import load_all_data, update_json_by_deleting_gif
from lexicon import lang_ru


router = Router()


@router.callback_query(F.data.split(':')[0] == 'delete')
async def any_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    gif_name = callback.data.split(':')[1]

    data = load_all_data(callback.message)
    del data[user_id]['gifs_data'][gif_name]

    update_json_by_deleting_gif(data)

    await callback.message.edit_caption(
        caption=lang_ru['deleted_gif']
    )


