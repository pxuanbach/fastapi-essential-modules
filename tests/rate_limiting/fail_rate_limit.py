import requests
import time
import asyncio
from datetime import datetime

url = "http://localhost:8000/api/v1/utils/limiting"
payload = ""

def send_request():
    response = requests.request("GET", url, data=payload)
    print(datetime.now(), response.text)
    time.sleep(0.5)

send_request()  # 1 at 0s
send_request()  # 2 at 0.5s
send_request()  # 3 at 1
send_request()  # 4 at 1.5s
send_request()  # 5 at 2s
send_request()  # 6 at 2.5s
send_request()  # 7 at 3s => fail
