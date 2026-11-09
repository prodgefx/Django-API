import requests

endpoint = "https://github.com"

response = requests.get(endpoint)

print(response.json())