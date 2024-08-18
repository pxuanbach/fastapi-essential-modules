import requests
import time
from datetime import datetime

url = "http://localhost:8000/api/v1/utils/limiting2"
payload = ""

def send_request():
    now = datetime.now()
    response = requests.request("GET", url, data=payload)
    print(now, response.text)
    time.sleep(0.5)

# On my local machine, the request take 2 seconds to get a response.
# Rule: 1/1m
send_request()  # R1 success at 2.5s, redis contains [R1]
send_request()  # R2 fails at 5s, redis contains [R1]

time.sleep(58)  # wait 55s, finish at 63s

send_request()  # R3 success at 65.5s, redis contains [R3]
