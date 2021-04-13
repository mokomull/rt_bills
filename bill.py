import copy
from datetime import datetime
from dateutils import relativedelta
from typing import Optional, Tuple


# TODO: this should be a dataclass but I don't get to use Python 3.7 yet
class Bill:
    def __init__(self, name: str, bill_available_day: int, bill_due_day: int):
        self.name = name
        self.bill_available_day = bill_available_day
        self.bill_due_day = bill_due_day

    def get_due_date_bounds(
        self,
        timestamp: Optional[datetime] = None
    ) -> Optional[Tuple[datetime, datetime]]:
        if timestamp is None:
            timestamp = datetime.utcnow()

        if self.bill_available_day < self.bill_due_day:
            # the bill-available date and due date are within the same month, so we should file a
            # ticket if it's currently between those days this month.
            file_ticket_bounds = (
                datetime(timestamp.year, timestamp.month,
                         self.bill_available_day),
                datetime(timestamp.year, timestamp.month, self.bill_due_day),
            )
        elif self.bill_due_day < self.bill_available_day:
            # the bill due day is in a different month than when the bill is available, so things
            # are a little more complicated.

            # start looking at the current month's bill
            file_ticket_bounds = (
                datetime(timestamp.year, timestamp.month,
                         self.bill_available_day) - relativedelta(months=1),
                datetime(timestamp.year, timestamp.month, self.bill_due_day),
            )

            # but if we're already after the due date this month, look at next month
            if timestamp > file_ticket_bounds[1]:
                file_ticket_bounds = tuple(i + relativedelta(months=1)
                                           for i in file_ticket_bounds)
        else:
            raise RuntimeError(
                "Bill is available on the same day it's due, and I don't know how to handle that yet."
            )

        if (timestamp > file_ticket_bounds[0]
                and timestamp < file_ticket_bounds[1]):
            last_month = file_ticket_bounds[1] - relativedelta(months=1)
            return (last_month, file_ticket_bounds[1])

        return None
