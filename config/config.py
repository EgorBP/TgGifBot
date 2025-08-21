from dataclasses import dataclass
from environs import Env
from aiogram.client.session.aiohttp import AiohttpSession


@dataclass
class TgBot:
    token: str
    session: AiohttpSession


@dataclass
class Config:
    tg_bot: TgBot
    api_base_url: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    # Использовалось при заливке на PythonAnywhere
    session = AiohttpSession(proxy='http://proxy.server:3128')

    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN'), session=session),
        api_base_url=env('API_BASE_URL')
    )