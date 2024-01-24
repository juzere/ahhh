from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.URLField(max_length=300, null=True, blank=True)
    


    def __str__(self):
        return self.nome

