import requests

url = "http://localhost:8000/api/v1/jobs"

payload = {
    "job_id": "log_with_args",
    "from_file": False,
    "type": "date",
    "args": {
        "run_date": "2024-04-20T18:45:48Z",
        "args": ["haha"]
    }
}
headers = {
    "Content-Type": "application/json",
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
