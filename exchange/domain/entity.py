import itertools
import textwrap
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from decimal import Decimal
from typing import TypeAlias

CharCode: TypeAlias = str


@dataclass(slots=True)
class Currency:
    id: str
    code: int
    char_code: CharCode
    nominal: int
    name: str
    value: Decimal
    vunit_rate: Decimal
    _info: str = field(init=False, default="")

    @property
    def info(self) -> str:
        if self._info:
            return self._info

        self._info = textwrap.dedent(f"""\
            <b>Id:</b> {self.id}
            <b>Code:</b> {self.code}
            <b>Char code:</b> {self.char_code}
            <b>Nominal:</b> {self.nominal}
            <b>Name:</b> {self.name}
            <b>Value:</b> {self.value}
            <b>Vunit rate:</b> {self.vunit_rate}
        """)
        return self._info

    def __str__(self) -> str:
        prep = f"{self.value:.2f}"
        return f"{self.char_code:4}{prep:>6} RUB"

    def __mul__(self, other: object, /) -> Decimal:
        if not isinstance(other, type(self)):
            raise TypeError(f"value should be {self.__class__.__name__}")

        return self.value * other.value

    def __truediv__(self, other: object, /) -> Decimal:
        if not isinstance(other, type(self)):
            raise TypeError(f"value should be {self.__class__.__name__}")

        return self.value / other.value


@dataclass(slots=True)
class CurrenciesBank:
    today: str
    _repository: dict[CharCode, Currency]
    _rates: str = field(init=False, default="")

    def __post_init__(self) -> None:
        rates = sorted(self, key=lambda cur: cur.value, reverse=True)
        formatted = self._formatting(rates)
        self._rates = f"<b>{self.today}</b>\n\n<code>{formatted}</code>"

    def __getitem__(self, item: object) -> Currency:
        if not isinstance(item, str):
            raise TypeError("value should be a string")

        return self._repository[item]

    def __iter__(self) -> Iterator[Currency]:
        yield from self._repository.values()

    def __contains__(self, value: object) -> bool:
        if not isinstance(value, str):
            raise TypeError("value should be a string")

        return value.upper() in self._repository

    def _formatting(self, currs: Iterable[Currency]) -> str:
        batch = itertools.batched(currs, 2)
        return "\n".join(f"{cur1}   {cur2}" for cur1, cur2 in batch)

    @property
    def rates(self) -> str:
        return self._rates

    def get(self, item: str) -> Currency | None:
        return self._repository.get(item)

    def convert(self, cur1: str, cur2: str) -> Decimal:
        convert = self[cur1] / self[cur2]
        return convert

    def exchange(self, cur1: str, cur2: str, amount: str) -> Decimal:
        return self.convert(cur1, cur2) * Decimal(amount)
