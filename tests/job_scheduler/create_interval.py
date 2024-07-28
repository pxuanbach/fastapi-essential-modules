import requests

url = "http://localhost:8000/api/v1/jobs"

payload = {
    "job_id": "log_something",
    "from_file": False,
    "type": "interval",
    "args": {"seconds": "15"}
}
headers = {
    "Content-Type": "application/json",
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
