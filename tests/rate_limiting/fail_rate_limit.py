import requests
import time
from datetime import datetime

url = "http://localhost:8000/api/v1/utils/limiting"
payload = ""

def send_request():
    response = requests.request("GET", url, data=payload)
    print(datetime.now(), response.text)
    time.sleep(1)

for i in range(6):
    send_request()  # fail at 6

time.sleep(13)  # fail
send_request()
