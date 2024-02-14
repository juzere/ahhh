from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Produto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
   
    imagem = models.URLField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.nome



class MedicaoVelocidade(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    velocidade = models.FloatField()

    def __str__(self):
        return f"{self.velocidade} - {self.data_hora.strftime('%Y-%m-%d %H:%M:%S')}"