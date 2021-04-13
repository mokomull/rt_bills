import datetime
from typing import Optional

# TODO: this should be a dataclass but I don't get to use Python 3.7 yet
class Bill:
    def __init__(self, name: str, bill_available_day: int, bill_due_day: int):
        self.name = name
        self.bill_available_day = bill_available_day
        self.bill_due_day = bill_due_day

    def get_due_date_bounds(self, timestamp: Optional[datetime.datetime]):
        if timestamp is None:
            timestamp = datetime.datetime.utcnow()

