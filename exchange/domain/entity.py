import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Self, TypeAlias

CharCode: TypeAlias = str
Serialized: TypeAlias = str | bytes | bytearray


class DecimalStr(str):
    def __new__(cls, value: Any) -> Self:
        return super().__new__(cls, value)

    def __init__(self, value: Any) -> None:
        super().__init__()
        self.val = Decimal(value.replace(",", ".", 1))

    def __mul__(self, other: Any, /) -> str:
        other = self.__class__(other)
        return str(self.val * other.val)

    def __truediv__(self, other: Any, /) -> str:
        other = self.__class__(other)
        return str(self.val / self.val)


class CurrencyEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Currency):
            return o.__dict__
        return super().default(o)


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
        return f"{self.char_code:<10}\t{self.value:.2f}\t{'RUB':>5}"

    def __truediv__(self, other: object, /) -> Decimal:
        if not isinstance(other, type(self)):
            raise TypeError("value should be itself")

        return Decimal(self.value) / Decimal(other.value)


@dataclass(slots=True)
class CurrenciesBank:
    today: str
    _repository: dict[CharCode, Currency]
    _rates: str = field(init=False, default="")

    def __post_init__(self) -> None:
        title = f"{'CODE':<10}RATE{'CY':>5}"
        rates = "\n".join(map(str, sorted(self, key=lambda x: x.value)))
        self._rates = f"<b>{self.today}\n\n{title}</b>\n<code>{rates}</code>"

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

    def to_json(self) -> Serialized:
        return json.dumps(self.__dict__, cls=CurrencyEncoder)

    @classmethod
    def from_json(cls, s: Serialized) -> Self:
        return cls(**json.loads(s, parse_float=Decimal))
