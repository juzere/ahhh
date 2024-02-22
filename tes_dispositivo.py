import requests

url = "http://127.0.0.1:8000//api/receber/"


usuario_id = 5

dados = {
    "velocidade": 55.2,
    "usuario_id": usuario_id
}


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
