import asyncio

from aiogram import Bot, Dispatcher
from environs import Env

from handlers import commands_handlers, functional_handlers
from states import storage


async def main():
    env = Env()
    env.read_env()
    bot_token = env('BOT_TOKEN')

    bot = Bot(token=bot_token)

    dp = Dispatcher(storage=storage)
    dp.include_router(commands_handlers.router)
    dp.include_router(functional_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())