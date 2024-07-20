import unittest
from decimal import Decimal

from exchange.domain.entity import DecimalStr


class TestDecimalStr(unittest.TestCase):
    def setUp(self) -> None:
        self.num_raw = "3,1415"
        self.num_dec = Decimal(self.num_raw.replace(",", "."))
        self.num = DecimalStr(self.num_raw)

    def test_equal(self) -> None:
        self.assertEqual(self.num.val, self.num_dec)

    def test_mul(self) -> None:
        r = str(self.num_dec * self.num_dec)
        self.assertEqual(self.num * self.num_raw, r)

    def test_div(self) -> None:
        r = str(self.num_dec / self.num_dec)
        self.assertEqual(self.num / self.num_raw, r)


if __name__ == "__main__":
    unittest.main()
