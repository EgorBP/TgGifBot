import asyncio
import datetime
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.handlers import callback_handlers, other_handlers
from bot.handlers import functional_handlers, user_handlers
from states import storage
from bot.config import config

logging.basicConfig(level=logging.INFO)
logging.getLogger("aiogram").setLevel(logging.WARNING)


async def main():
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        # session=config.tg_bot.session,
    )

    dp = Dispatcher(storage=storage)
    dp.include_routers(
        user_handlers.router,
        functional_handlers.router,
        callback_handlers.router,
        other_handlers.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.info(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Successfully started!")
    asyncio.run(main())
