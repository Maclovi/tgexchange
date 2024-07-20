from typing import cast

import aiohttp


async def get_raw_response(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        xml_raw = await resp.read()

    return cast(bytes, xml_raw)
