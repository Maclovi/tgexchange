from collections.abc import AsyncIterator
from typing import cast

from exchange.domain.entity import CurrenciesBank, Currency

from .parse import iter_xmldata


async def get_currencies() -> CurrenciesBank:
    iter_xml = iter_xmldata()
    today = cast(str, await iter_xml.__anext__())
    iter_xml = cast(AsyncIterator[Currency], iter_xml)

    return CurrenciesBank(today, {xml.char_code: xml async for xml in iter_xml})
