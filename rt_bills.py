import sys

import requests.auth
import rt

from bill import Bill

USER = "billsbot"
PASSWORD = "8hb8kobooPamMaEwTjfq"

BILLS = [
    Bill("Verizon", 26, 15),
]

# for some reason, I set up HTTP Basic authentication in front of the
# application, AND required a password sent
tracker = rt.Rt(
    "https://mmlx.us/rt/REST/1.0",
    USER,
    PASSWORD,
    http_auth=requests.auth.HTTPBasicAuth(USER, PASSWORD),
)
if not tracker.login():
    print("Failed to log in", file=sys.stderr)

for bill in BILLS:
    bounds = bill.get_due_date_bounds()

    if bounds is None:
        continue

    tickets = tracker.search(
        Queue=12,
        Format="i",
        Subject__exact=bill.name,
        Due__gt=bounds[0].strftime("%Y-%m-%d"),
        Due__le=bounds[1].strftime("%Y-%m-%d"),
    )

    if len(tickets) == 0:
        print("Creating a new ticket for {}".format(bill.name),
              file=sys.stderr)
        tracker.create_ticket(
            Queue="Bills",
            Subject=bill.name,
            Owner="mmullins",
            Due=bounds[1].strftime("%Y-%m-%d"),
        )
    else:
        print("Already found ticket for {}".format(bill.name), file=sys.stderr)