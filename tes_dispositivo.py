import requests

# URL da API para a qual você está enviando os dados
url = "http://127.0.0.1:8000/api/receber/"

# Atualize esta seção para incluir o 'usuario_id' junto aos dados de velocidade
# Substitua '1' pelo ID do usuário apropriado que você deseja simular
dados = {
    "velocidade": 60.2,
    "usuario_id": 5
}

# Fazendo a requisição POST para a API
response = requests.post(url, json=dados)

# Verificando a resposta
if response.status_code == 200:
    try:
        # Tentando extrair e imprimir a resposta JSON
        data = response.json()
        print("Response:", data)
    except Exception as e:
        print("Failed to parse JSON:", str(e))
else:
    print("Status Code:", response.status_code)
    print("Response:", response.text)

