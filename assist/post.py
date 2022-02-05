import requests

url = "https://accounts.havail.sabre.com/login/srw"

payload = "goto=https%3A%2F%2Fsrw.sabre.com%2Flogin%2Flogin.html%3Fts%3D555880&siteId=srw&userId=1004&password=1A2B3C4D&group=2Q4J&_csrf=2bb71971-7a09-482d-89bb-f73fce9e6d52&undefined="
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Postman-Token': "6a8fdb5e-8a70-4dc9-b278-3308c5d08f29"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.raw.headers.getlist('Set-Cookie'))