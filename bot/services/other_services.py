from aiogram.types import Message
from bot.keyboards import BotInlineKeyboard


async def send_gif_with_inline_keyboard(message: Message, tg_gif_id: str, tags: list[str], inline_markup: BotInlineKeyboard):
    await message.answer_animation(
        tg_gif_id,
        caption=f'<b>Теги:</b>  {tags}',
        reply_markup=inline_markup.keyboard_gif_edit(),
    )
