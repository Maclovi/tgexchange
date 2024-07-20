import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiohttp import ClientSession

from exchange.bot.handlers import user
from exchange.config import load_config
from exchange.ioc import Ioc

logger = logging.getLogger(__name__)


async def tgbot_main() -> None:
    conf = load_config()

    level = logging.DEBUG if conf.tg_bot.debug else logging.INFO
    logging.basicConfig(level=level, stream=sys.stdout)

    session = ClientSession()
    storage = RedisStorage.from_url(conf.redis.get_uri())

    ioc: Ioc = Ioc(session=session, redis=storage.redis)

    bot = Bot(token=conf.tg_bot.token)
    dp = Dispatcher(storage=storage, ioc=ioc)
    dp.include_router(user.router)

    try:
        await storage.redis.ping()
        await dp.start_polling(bot)
    finally:
        await ioc.session.close()
        await ioc.redis.aclose()  # type: ignore


def cli() -> None:
    """Wrapper for command line"""
    asyncio.run(tgbot_main())


if __name__ == "__main__":
    cli()
