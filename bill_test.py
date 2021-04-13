import unittest
from datetime import datetime

from bill import Bill

FIRST = datetime(2021, 4, 1, 0, 0, 0)
FIFTEENTH = datetime(2021, 4, 15, 0, 0, 0)
TWENTYSEVENTH = datetime(2021, 4, 27, 0, 0, 0)


class BilledAndDueInSameMonth(unittest.TestCase):
    bill = Bill("DueInSameMonth", 2, 25)

    def test_first(self):
        self.assertIsNone(self.bill.get_due_date_bounds(FIRST))

    def test_fifteenth(self):
        self.assertEqual(
            self.bill.get_due_date_bounds(FIFTEENTH),
            (
                datetime(2021, 3, 25),
                datetime(2021, 4, 25),
            ),
        )

    def test_twentyseventh(self):
        self.assertIsNone(self.bill.get_due_date_bounds(TWENTYSEVENTH))


class DueMonthAfterBilling(unittest.TestCase):
    bill = Bill("DueNextMonth", 26, 15)

    def test_first(self):
        self.assertEqual(
            self.bill.get_due_date_bounds(FIRST),
            (
                datetime(2021, 3, 15),
                datetime(2021, 4, 15),
            ),
        )

    def test_fifteenth(self):
        self.assertIsNone(self.bill.get_due_date_bounds(FIFTEENTH))

    def test_twentyseventh(self):
        self.assertEqual(
            self.bill.get_due_date_bounds(TWENTYSEVENTH),
            (
                datetime(2021, 4, 15),
                datetime(2021, 5, 15),
            ),
        )


class DueOnFirstOfTheMonth(unittest.TestCase):
    bill = Bill("Rent", 25, 1)

    def test_first(self):
        self.assertIsNone(self.bill.get_due_date_bounds(FIRST))

    def test_fifteenth(self):
        self.assertIsNone(self.bill.get_due_date_bounds(FIFTEENTH))

    def test_twentyseventh(self):
        self.assertEqual(
            self.bill.get_due_date_bounds(TWENTYSEVENTH),
            (
                datetime(2021, 4, 1),
                datetime(2021, 5, 1),
            ),
        )


class AfterDecember(unittest.TestCase):
    bill = Bill("DueInJanuary", 25, 15)

    def test_dec10(self):
        self.assertEqual(
            self.bill.get_due_date_bounds(datetime(2019, 12, 10)),
            (
                datetime(2019, 11, 15),
                datetime(2019, 12, 15),
            ),
        )

    def test_dec16(self):
        self.assertIsNone(
            self.bill.get_due_date_bounds(datetime(2019, 12, 16), ))

    def test_dec25(self):
        self.assertEqual(
            self.bill.get_due_date_bounds(datetime(2019, 12, 25, 0, 0, 1)),
            (
                datetime(2019, 12, 15),
                datetime(2020, 1, 15),
            ),
        )

    def test_jan1(self):
        self.assertEqual(
            self.bill.get_due_date_bounds(datetime(2020, 1, 1)),
            (
                datetime(2019, 12, 15),
                datetime(2020, 1, 15),
            ),
        )


if __name__ == "__main__":
    unittest.main()
