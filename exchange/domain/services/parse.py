import xml.etree.ElementTree as ElemTree
from collections.abc import AsyncIterator
from functools import partial
from typing import cast

from exchange.domain.entity import Currency
from exchange.helpers import get_raw_response, to_decimal


def get_text_by_node(node: ElemTree.Element, path: str, /) -> str:
    element = cast(ElemTree.Element, node.find(path))
    return str(element.text)


async def iter_xmldata() -> AsyncIterator[Currency | str]:
    xml_raw = await get_raw_response("https://cbr.ru/scripts/XML_daily.asp")
    tree = ElemTree.fromstring(xml_raw)

    today = tree.get("Date")
    yield f"Central Bank rate on {today}"

    yield Currency(
        id="RAKETAHAXYI",
        code=643,
        char_code="RUB",
        nominal=1,
        name="Российский рубль",
        value=to_decimal("1"),
        vunit_rate=to_decimal("1"),
    )

    for node in tree.iter("Valute"):
        by_node = partial(get_text_by_node, node)

        yield Currency(
            id=node.get("ID", "no id"),
            code=int(by_node("NumCode")),
            char_code=by_node("CharCode"),
            nominal=int(by_node("Nominal")),
            name=by_node("Name"),
            value=to_decimal(by_node("Value")),
            vunit_rate=to_decimal(by_node("VunitRate")),
        )
