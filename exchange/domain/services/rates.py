import logging
from collections.abc import Iterator
from typing import TYPE_CHECKING, TypeAlias, cast

from exchange.domain.entity import CurrenciesBank, Currency
from exchange.domain.services.parse import parse_xml

if TYPE_CHECKING:
    from exchange.ioc import Ioc


logger = logging.getLogger(__name__)

Today: TypeAlias = str
ParsedXml: TypeAlias = tuple[Today, Iterator[Currency]]


class Rates:
    def __init__(self, ioc: "Ioc") -> None:
        self.ioc = ioc
        self.key = "bank"
        self.url = "https://cbr.ru/scripts/XML_daily.asp"

    async def get_url_xml(self, url: str) -> bytes:
        logger.info("Xml returned from url")
        resp = await self.ioc.session.get(url)
        return cast(bytes, await resp.read())

    async def get_redis_xml(self, key: str) -> bytes | None:
        return await self.ioc.redis.get(key)

    async def set_redis_xml(self, key: str, xml: bytes) -> bool:
        await self.ioc.redis.set(key, xml, ex=86_000)
        return True

    async def key_exists(self, key: str) -> bool:
        return bool(await self.ioc.redis.exists(key))

    async def get_xml(self) -> bytes:
        if xml := await self.get_redis_xml(self.key):
            logger.info("Xml returned from redis")
            return xml

        xml = await self.get_url_xml(self.url)

        logger.info("Write the xml to redis cache")
        await self.set_redis_xml(self.key, xml)

        return xml

    def get_parsed_currencies(self, xml: bytes) -> ParsedXml:
        xmlcurrency = parse_xml(xml)
        today = cast(str, next(xmlcurrency))
        return today, cast(Iterator[Currency], xmlcurrency)

    def init_currenciesbank(self, xml: bytes) -> CurrenciesBank:
        logger.info("Parse the xml & Initialize the CurrenciesBank")
        today, currencies = self.get_parsed_currencies(xml)
        return CurrenciesBank(today, {xml.char_code: xml for xml in currencies})

    async def get_bank(self) -> CurrenciesBank:
        if (bank := self.ioc.bank) and await self.key_exists(self.key):
            logger.info("Bank returned from python object")
            return bank

        xml = await self.get_xml()
        bank = self.init_currenciesbank(xml)
        self.ioc.bank = bank

        return bank
