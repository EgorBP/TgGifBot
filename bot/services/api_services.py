from bot.config import config
from typing import Sequence
import aiohttp
from bot.schemas import ResponseModel


async def search_user_gifs(tg_user_id: int, gif_tags: Sequence[str] | None = None):
    """
    Получить список GIF пользователя с сервера по Telegram ID и опциональным тегам.

    Args:
        tg_user_id (int): Telegram ID пользователя, для которого ищем GIF.
        gif_tags (Sequence[str] | None, optional): Список тегов для фильтрации GIF.
            Если не передан, возвращаются все GIF пользователя.

    Returns:
        ResponseModel: Объект с данными от API и HTTP-статусом ответа.
    """
    if gif_tags:
        tags_request = '&tags=' + '&tags='.join(gif_tags)
    else:
        tags_request = ''
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{config.api_base_url}/search?tg_user_id={tg_user_id}{tags_request}') as response:
            data = await response.json()
            return ResponseModel(data=data, code=response.status)


async def update_user_gif_tags(tg_user_id: int, tg_gif_id: str, gif_tags: Sequence[str]):
    """
    Обновить список тегов у конкретного GIF пользователя на сервере.

    Args:
        tg_user_id (int): Telegram ID пользователя.
        tg_gif_id (str): Идентификатор GIF в Telegram.
        gif_tags (Sequence[str]): Список тегов для присвоения GIF.

    Returns:
        ResponseModel: Объект с данными от API и HTTP-статусом ответа.
    """
    data_json = {'tags': gif_tags}
    async with aiohttp.ClientSession() as session:
        async with session.put(f'{config.api_base_url}/user/{tg_user_id}/gif/{tg_gif_id}', json=data_json) as response:
            data = await response.json()
            return ResponseModel(data=data, code=response.status)


async def get_all_user_tags(tg_user_id: int):
    """
    Получить все теги пользователя с сервера по Telegram ID.

    Args:
        tg_user_id (int): Telegram ID пользователя.

    Returns:
        ResponseModel: Объект с данными от API и HTTP-статусом ответа.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{config.api_base_url}/user/{tg_user_id}/tags') as response:
            data = await response.json()
            return ResponseModel(data=data, code=response.status)


async def delete_user_gif(tg_user_id: int, db_gif_id: int):
    """
    Удалить GIF пользователя на сервере по его внутреннему ID в базе.

    Args:
        tg_user_id (int): Telegram ID пользователя.
        db_gif_id (int): Внутренний ID GIF в базе данных.

    Returns:
        ResponseModel: Объект с данными от API и HTTP-статусом ответа.
    """
    async with aiohttp.ClientSession() as session:
        async with session.delete(f'{config.api_base_url}/user/{tg_user_id}/gif/{db_gif_id}?gif_id_type=db') as response:
            data = await response.json()
            return ResponseModel(data=data, code=response.status)
