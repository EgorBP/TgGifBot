import pytest
from bot.config import config
import aiohttp
from aiohttp import ClientConnectionError


@pytest.mark.asyncio
async def test_api_connection():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{config.api_base_url}') as response:
                assert response.status < 500
    except ClientConnectionError:
        pytest.fail("Не удалось подключиться к API")
