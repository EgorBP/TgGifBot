from config import config
from typing import Sequence
import aiohttp
from schemas import ResponseModel


async def search_user_gifs(tg_user_id: int, gif_tags: Sequence[str] | None = None):
    async with aiohttp.ClientSession() as session:
        if gif_tags:
            tags_request = '&tags=' + '&tags='.join(gif_tags)
        else:
            tags_request = ''
        async with session.get(f'{config.api_base_url}/search?tg_user_id={tg_user_id}{tags_request}') as response:
            data = await response.json()
            return ResponseModel(data=data, code=response.status)


async def update_user_gif_tags(tg_user_id: int, tg_gif_id: str, gif_tags: Sequence[str]):
    async with aiohttp.ClientSession() as session:
        data_json = {'tags': gif_tags}
        async with session.put(f'{config.api_base_url}/user/{tg_user_id}/gif/{tg_gif_id}', json=data_json) as response:
            data = await response.json()
            return ResponseModel(data=data, code=response.status)


async def get_all_user_tags(tg_user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{config.api_base_url}/user/{tg_user_id}/tags') as response:
            data = await response.json()
            return ResponseModel(data=data, code=response.status)


async def delete_user_gif(tg_user_id: int, db_gif_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.delete(f'{config.api_base_url}/user/{tg_user_id}/gif/{db_gif_id}?gif_id_type=db') as response:
            data = await response.json()
            return ResponseModel(data=data, code=response.status)
