import requests

url = "http://localhost:8000/api/v1/jobs"

payload = {
    "job_id": "get_random_user",
    "from_file": True,
    "type": "cron",
    # "args": {
    #     "year": "*",
    #     "month": "*",
    #     "day": "*",
    #     "week": "*",
    #     "day_of_week": "*",
    #     "hour": "*",
    #     "minute": "*",
    #     "second": "15"
    # }
}
headers = {
    "Content-Type": "application/json",
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
