import requests
import time
from datetime import datetime

url = "http://localhost:8000/api/v1/utils/limiting1"
payload = ""

def send_request():
    now = datetime.now()
    response = requests.request("GET", url, data=payload)
    print(now, response.text)
    time.sleep(0.5)

# On my local machine, the request take 2 seconds to get a response.
# Rule: 5/15s
send_request()  # R1 success at 2.5s, redis contains [R1]
send_request()  # R2 success at 5s, redis contains [R1, R2]
send_request()  # R3 success at 7.5s, redis contains [R1, R2, R3]
send_request()  # R4 success at 10s, redis contains [R1, R2, R3, R4]
send_request()  # R5 success at 12.5s, redis contains [R1, R2, R3, R4, R5]
send_request()  # R6 fails at 15s, redis contains [R1, R2, R3, R4, R5]
send_request()  # R7 success at 18.5s, redis contains [R2, R3, R4, R5, R7]
