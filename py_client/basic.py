import requests

endpoint = "http://127.0.0.1:8000/api/"
response = requests.post(endpoint, json={
    "title": "Bananas",
    "content": "Fresh fruit",
    "price": 2.99,
    "sale_price": 2.50
})

print(response.status_code)
print(response.json())  