import itertools
import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Self, TypeAlias

CharCode: TypeAlias = str
Serialized: TypeAlias = str | bytes | bytearray


class CurrencyEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Currency):
            return o.__dict__
        return super().default(o)


class DecimalStr(str):
    def __new__(cls, val: Any) -> Self:
        return super().__new__(cls, val)

    def __init__(self, val: Any) -> None:
        super().__init__()
        val = val.replace(",", ".", 1) if isinstance(val, str) else val
        self.dec = Decimal(val)

    def __mul__(self, other: Any, /) -> Self:
        if not isinstance(other, type(self)):
            other = self.__class__(other)
        return self.__class__(self.dec * other.dec)

    def __truediv__(self, other: Any, /) -> Self:
        if not isinstance(other, type(self)):
            other = self.__class__(other)
        return self.__class__(self.dec / other.dec)


@dataclass(slots=True, frozen=True)
class Currency:
    id: str
    code: int
    char_code: CharCode
    nominal: int
    name: str
    value: DecimalStr
    vunit_rate: DecimalStr

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError("value should be itself")

        return self.char_code == other.char_code

    def __hash__(self) -> int:
        return hash(self.char_code)

    def __str__(self) -> str:
        prep = f"{self.value.dec:.2f}"
        return f"{self.char_code:4}{prep:>6} RUB"

    def __mul__(self, other: object, /) -> DecimalStr:
        if not isinstance(other, type(self)):
            raise TypeError("value should be itself")

        return self.value * other.value

    def __truediv__(self, other: object, /) -> DecimalStr:
        if not isinstance(other, type(self)):
            raise TypeError("value should be itself")

        return self.value / other.value


@dataclass(slots=True)
class CurrenciesBank:
    today: str
    _repository: dict[CharCode, Currency]
    _rates: str = field(init=False, default="")

    def __post_init__(self) -> None:
        rates = sorted(self, key=lambda cur: cur.value.dec)
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

    def convert(self, cur1: str, cur2: str) -> DecimalStr:
        convert = self[cur1] / self[cur2]
        return convert

    def exchange(self, cur1: str, cur2: str, amount: str) -> DecimalStr:
        return self.convert(cur1, cur2) * amount

    def to_json(self) -> Serialized:
        return json.dumps(self.__dict__, cls=CurrencyEncoder)

    @classmethod
    def from_json(cls, s: Serialized) -> Self:
        return cls(**json.loads(s, parse_float=Decimal))
