from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from redis.asyncio.client import Redis

    from exchange.domain.entity import CurrenciesBank


@dataclass
class Ioc:
    session: "ClientSession"
    redis: "Redis"  # type: ignore
    bank: "CurrenciesBank | None" = None
