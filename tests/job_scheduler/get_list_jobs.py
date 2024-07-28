import requests

url = "http://localhost:8000/api/v1/jobs"

payload = ""
headers = {
    "Content-Type": "application/json",
}

response = requests.request("GET", url, data=payload, headers=headers)

print(response.text)
