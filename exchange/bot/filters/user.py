import logging
from typing import TYPE_CHECKING, TypeAlias, cast

from aiogram.filters import KICKED, MEMBER, ChatMemberUpdatedFilter, Filter
from aiogram.filters import CommandStart as CommandStart
from aiogram.types import Message as Msg

from exchange.domain.services.rates import Rates

if TYPE_CHECKING:
    from exchange.domain.entity import CurrenciesBank
    from exchange.ioc import Ioc

logger = logging.getLogger(__name__)

IF_KICKED = ChatMemberUpdatedFilter(member_status_changed=KICKED)
IF_MEMBER = ChatMemberUpdatedFilter(member_status_changed=MEMBER)


Inject: TypeAlias = "bool | dict[str, CurrenciesBank]"


class ChatIsPrivate(Filter):
    async def __call__(self, msg: Msg) -> bool:
        return bool(msg.chat.type == "private")


class CommandForCurrency(Filter):
    def __init__(self, command: str, /) -> None:
        super().__init__()
        self.command = command

    async def __call__(self, msg: Msg, ioc: "Ioc") -> Inject:
        txt = cast(str, msg.text)
        if not txt.startswith(self.command):
            return False

        return {"bank": await Rates(ioc).get_bank()}
