import logging
import textwrap
from typing import TYPE_CHECKING, cast

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import ChatMemberUpdated, Message

from ..filters.user import (
    IF_KICKED,
    IF_MEMBER,
    ChatIsPrivate,
    CommandForCurrency,
)

if TYPE_CHECKING:
    from exchange.domain.entity import CurrenciesBank as Bank


logger = logging.getLogger(__name__)
router = Router()
router.message.filter(ChatIsPrivate())


@router.message(CommandStart())
async def proccess_cmd_start(message: Message) -> None:
    logger.info("Do proccess_cmd_start")

    await message.answer("Здарова пёс")


@router.message(CommandForCurrency("/exchange"))
async def currency_convert(message: Message, bank: "Bank") -> None:
    txt = cast(str, message.text)
    _, *args = txt.upper().split()

    if not args or len(args) != 3:
        await message.answer("Заебал хуйнёй страдать, передай 2 аргумента")
    elif not (args[0] in bank and args[1] in bank):
        await message.answer("Нет такой валюты уебан")
    elif not args[-1].isdigit():
        await message.answer("Вздумал наебать меня?")
    else:
        cur1, cur2, amount = args
        exch = bank.exchange(cur1, cur2, amount)
        conv1 = bank.convert(cur1, cur2)
        conv2 = bank.convert(cur2, cur1)

        resp = textwrap.dedent(f"""\
            {bank.today}

            <b>{amount} {cur1} to {cur2}</b>
            1 {cur1} = {conv1:.2f} {cur2}   1 {cur2} = {conv2:.2f} {cur1}
            {amount} {cur1} = {cur2} {exch:.2f}
        """)

        await message.answer(resp, parse_mode="HTML")


@router.message(CommandForCurrency("/rates"))
async def get_rates(message: Message, bank: "Bank") -> None:
    await message.answer(bank.rates, parse_mode="HTML")


@router.my_chat_member(IF_KICKED)
async def process_user_blocked_bot(_: ChatMemberUpdated) -> None:
    logger.info("Do process_user_blocked_bot")
    logger.info("Съебался")


@router.my_chat_member(IF_MEMBER)
async def process_user_unblocked_bot(event: ChatMemberUpdated) -> None:
    logger.info("Do process_user_unblocked_bot")

    await event.answer("Zdarov")


@router.message()
async def send_other(message: Message) -> None:
    logger.info("Do send_other")

    await message.answer("Ты высрал какую-то хуйню")
