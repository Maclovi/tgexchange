import unittest
from decimal import Decimal

from exchange.domain.entity import DecimalStr


class TestDecimalStr(unittest.TestCase):
    def setUp(self) -> None:
        self.num_raw = "3,1415"
        self.num_dec = Decimal(self.num_raw.replace(",", "."))
        self.num = DecimalStr(self.num_raw)

    def test_equal(self) -> None:
        self.assertEqual(self.num.dec, self.num_dec)

    def test_mul(self) -> None:
        second = str(self.num_dec * self.num_dec)
        self.assertEqual(self.num * self.num_raw, second)

    def test_div(self) -> None:
        second = str(self.num_dec / self.num_dec)
        self.assertEqual(self.num / self.num_raw, second)

    def test_str_display(self) -> None:
        self.assertEqual(self.num, self.num_raw)

    def test_str_display2(self) -> None:
        self.assertNotEqual(DecimalStr("1.1"), "1,1")

    def test_int_display(self) -> None:
        self.assertEqual(DecimalStr(1), "1")

    def test_float_display(self) -> None:
        self.assertEqual(DecimalStr(1.1), "1.1")


if __name__ == "__main__":
    unittest.main()
