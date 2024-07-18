from collections.abc import Iterator
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class Currency:
    id: str
    code: int
    char_code: str
    nominal: int
    name: str
    value: Decimal
    vunit_rate: Decimal

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
        return self.value / other.value


@dataclass(slots=True)
class CurrenciesBank:
    today: str
    _repository: dict[str, Currency]
    _rates: str = field(init=False, default="")

    def __post_init__(self) -> None:
        self.today = f"<b>{self.today}</b>"
        title = f"<b>{'CODE':<10}RATE{'CY':>5}</b>"
        rates = "\n".join(self)
        self._rates = f"{self.today}\n\n{title}\n{rates}"

    def __getitem__(self, item: object) -> Currency:
        if not isinstance(item, str):
            raise TypeError("value should be a string")

        return self._repository[item]

    def __iter__(self) -> Iterator[str]:
        for d in self._repository.values():
            yield str(d)

    def __contains__(self, value: object) -> bool:
        if not isinstance(value, str):
            raise TypeError("value should be a string")

        return value.upper() in self._repository

    def get(self, item: str) -> Currency | None:
        return self._repository.get(item)

    @property
    def rates(self) -> str:
        return self._rates

    def convert(self, cur1: str, cur2: str) -> Decimal:
        convert = self[cur1] / self[cur2]
        return convert

    def exchange(self, cur1: str, cur2: str, amount: str) -> Decimal:
        return self.convert(cur1, cur2) * Decimal(amount)
