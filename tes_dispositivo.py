import requests

url = "http://127.0.0.1:8000/api/receber/"
dados = {"velocidade": 60.2}

response = requests.post(url, json=dados)

if response.status_code == 200:
    try:
        data = response.json()
        print("Response:", data)
    except Exception as e:
        print("Failed to parse JSON:", str(e))
else:
    print("Status Code:", response.status_code)
    print("Response:", response.text)
