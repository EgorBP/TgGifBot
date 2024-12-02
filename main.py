import asyncio
import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import user_handlers, functional_handlers, callback_handlers, other_handlers
from states import storage
from config import load_config


async def main():

    """ Питонячий скрипт """

    bot = Bot(
        token=load_config().tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        # session=load_config().tg_bot.session,
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
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Successfully started!")
    asyncio.run(main())
