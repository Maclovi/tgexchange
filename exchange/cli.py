import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from exchange.bot.handlers import user
from exchange.config import load_config

logger = logging.getLogger(__name__)


async def tgbot_main() -> None:
    conf = load_config()

    level = logging.DEBUG if conf.tg_bot.debug else logging.INFO
    logging.basicConfig(level=level, stream=sys.stdout)

    storage = RedisStorage.from_url(conf.redis.get_uri())
    await storage.redis.ping()

    bot = Bot(token=conf.tg_bot.token)
    dp = Dispatcher(storage=storage, storage2=storage)
    dp.include_router(user.router)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


def cli() -> None:
    """Wrapper for command line"""
    asyncio.run(tgbot_main())


if __name__ == "__main__":
    cli()
