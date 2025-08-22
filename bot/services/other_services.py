from aiogram.types import Message
from bot.keyboards import BotInlineKeyboard


async def send_gif_with_inline_keyboard(
        message: Message,
        tg_gif_id: str,
        tags: str,
        inline_markup: BotInlineKeyboard
):
    """
    Отправить GIF с подписями тегов и inline-кнопками.

    Args:
        message (Message): Объект сообщения Aiogram, куда отправляется GIF.
        tg_gif_id (str): Идентификатор GIF в Telegram.
        tags (str): Список тегов для отображения в подписи одной строкой.
        inline_markup (BotInlineKeyboard): Inline-клавиатура для GIF.

    Returns:
        None
    """
    await message.answer_animation(
        tg_gif_id,
        caption=f'<b>Теги:</b>  {tags}',
        reply_markup=inline_markup.keyboard_gif_edit(),
    )
