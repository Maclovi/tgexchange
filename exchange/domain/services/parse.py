import xml.etree.ElementTree as ElemTree
from collections.abc import Iterator
from decimal import Decimal
from functools import partial
from typing import cast

from exchange.domain.entity import Currency


def get_text_by_node(node: ElemTree.Element, path: str, /) -> str:
    element = cast(ElemTree.Element, node.find(path))
    return str(element.text)


def to_decimal(num: str) -> Decimal:
    return Decimal(num.replace(",", ".", 1))


def parse_xml(xml_raw: bytes) -> Iterator[Currency | str]:
    tree = ElemTree.fromstring(xml_raw)

    today = tree.get("Date")
    yield f"Central Bank rate on {today}"

    yield Currency(
        id="RAKETAHAXYI",
        code=643,
        char_code="RUB",
        nominal=1,
        name="Российский рубль",
        value=Decimal(1),
        vunit_rate=Decimal(1),
    )

    for node in tree.iter("Valute"):
        text_by_node = partial(get_text_by_node, node)

        yield Currency(
            id=node.get("ID", "no id"),
            code=int(text_by_node("NumCode")),
            char_code=text_by_node("CharCode"),
            nominal=int(text_by_node("Nominal")),
            name=text_by_node("Name"),
            value=to_decimal(text_by_node("Value")),
            vunit_rate=to_decimal(text_by_node("VunitRate")),
        )
