import requests

headers = {
    'Authorization': 'Bearer 0c798eda062294b22e9aa6279a6d8eca67331570'
}
endpoint = "http://127.0.0.1:8000/api/products/"

data = {
    "title": "LG TV",
    "content": "67' display",
    "price": 2500.00,
    }

get_response = requests.post(endpoint, json=data, headers=headers)

print(get_response.status_code)
print(get_response.json())