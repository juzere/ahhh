import pandas as pd
from django.contrib.auth.models import User
from aaaa.models import MedicaoVelocidade  

def importar_dados(planilha):
    df = pd.read_csv(planilha)
    
    for _, linha in df.iterrows():
        usuario_id = linha['id_usuario']
        dispositivo_id = linha['id_dispositivo']
        velocidade = linha['velocidade']
        data_hora = pd.to_datetime(linha['data_hora'])
        
        try:
            usuario = User.objects.get(id=usuario_id)
            MedicaoVelocidade.objects.create(
                usuario=usuario,
                dispositivo_id=dispositivo_id,
                velocidade=velocidade,
                data_hora=data_hora
            )
            print(f"Medição importada com sucesso para o usuário {usuario_id}.")
        except User.DoesNotExist:
            print(f"Usuário {usuario_id} não encontrado.")

importar_dados('planilha.csv')