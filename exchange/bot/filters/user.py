import logging
import pickle
from typing import TYPE_CHECKING, TypeAlias, cast

from aiogram.filters import KICKED, MEMBER, ChatMemberUpdatedFilter, Filter
from aiogram.filters import CommandStart as CommandStart
from aiogram.types import Message as Msg

from exchange.domain.services.rates import get_currencies

if TYPE_CHECKING:
    from aiogram.fsm.storage.redis import RedisStorage as Storage

    from exchange.domain.entity import CurrenciesBank as Bank

logger = logging.getLogger(__name__)

IF_KICKED = ChatMemberUpdatedFilter(member_status_changed=KICKED)
IF_MEMBER = ChatMemberUpdatedFilter(member_status_changed=MEMBER)

DictRepo: TypeAlias = dict[str, "Bank"]


class ChatIsPrivate(Filter):  # type: ignore
    async def __call__(self, msg: Msg) -> bool:
        return bool(msg.chat.type == "private")


class CommandForCurrency(Filter):  # type: ignore
    def __init__(self, command: str, /) -> None:
        super().__init__()
        self.command = command

    async def __call__(self, msg: Msg, storage2: "Storage") -> bool | DictRepo:
        txt = cast(str, msg.text)
        if not txt.startswith(self.command):
            return False

        key = "bank"
        if bank := await storage2.redis.get(key):
            return {key: pickle.loads(bank)}

        bank = await get_currencies()
        await storage2.redis.set(key, pickle.dumps(bank), ex=86_000)
        return {key: bank}
