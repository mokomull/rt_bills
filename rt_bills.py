import sys

import requests.auth
import rt

USER = "billsbot"
PASSWORD = "8hb8kobooPamMaEwTjfq"

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
