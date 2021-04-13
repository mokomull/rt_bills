import unittest
import datetime

from bill import Bill

FIRST = datetime.datetime(2021, 4, 1, 0, 0, 0)
FIFTEENTH = datetime.datetime(2021, 4, 15, 0, 0, 0)
TWENTYSEVENTH = datetime.datetime(2021, 4, 27, 0, 0, 0)


class BilledAndDueInSameMonth(unittest.TestCase):
    bill = Bill("DueInSameMonth", 2, 25)

    def test_first(self):
        self.assertIsNone(self.bill.get_due_date_bounds(FIRST))

    def test_fifteenth(self):
        self.assertEqual(
            self.bill.get_due_date_bounds(FIFTEENTH),
            (
                datetime.datetime(2021, 3, 25),
                datetime.datetime(2021, 4, 25),
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
                datetime.datetime(2021, 3, 15),
                datetime.datetime(2021, 4, 15),
            ),
        )

    def test_fifteenth(self):
        self.assertIsNone(self.bill.get_due_date_bounds(FIFTEENTH))

    def test_twentyseventh(self):
        self.assertEqual(
            self.bill.get_due_date_bounds(TWENTYSEVENTH),
            (
                datetime.datetime(2021, 4, 15),
                datetime.datetime(2021, 5, 15),
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
                datetime.datetime(2021, 4, 1),
                datetime.datetime(2021, 5, 1),
            ),
        )


if __name__ == "__main__":
    unittest.main()
