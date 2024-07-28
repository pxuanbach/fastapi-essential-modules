import requests

url = "http://localhost:8000/api/v1/jobs/get_random_user"

payload = ""
headers = {
    "Content-Type": "application/json",
}

response = requests.request("DELETE", url, data=payload, headers=headers)

print(response.text)
