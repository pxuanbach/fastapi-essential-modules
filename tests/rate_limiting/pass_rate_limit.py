import requests
import time
from datetime import datetime

url = "http://localhost:8000/api/v1/utils/limiting"
payload = ""

def send_request():
    response = requests.request("GET", url, data=payload)
    print(datetime.now(), response.text)
    time.sleep(1)

for i in range(5):
    send_request()

time.sleep(15)
send_request()
