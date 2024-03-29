
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetCompleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, LoginForm
from django.contrib import messages
from .models import Produto
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.utils.dateparse import parse_date
from rest_framework.response import Response
from .models import MedicaoVelocidade
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 

import json
from django.shortcuts import render

@login_required
def meus_produtos(request):
    produtos = Produto.objects.filter(usuario=request.user)
    dispositivos = MedicaoVelocidade.objects.filter(usuario=request.user).values_list('dispositivo_id', flat=True).distinct()
    dispositivo_selecionado = request.GET.get('dispositivo_id')

    
    if dispositivo_selecionado:
        medicoes = MedicaoVelocidade.objects.filter(usuario=request.user, dispositivo_id=dispositivo_selecionado)
    else:
        medicoes = MedicaoVelocidade.objects.none()  

    datas_json = json.dumps([medicao.data_hora.strftime('%Y-%m-%d %H:%M') for medicao in medicoes])
    velocidades_json = json.dumps([medicao.velocidade for medicao in medicoes])

    return render(request, 'meus_produtos.html', {
        'produtos': produtos,
        'dispositivos': dispositivos,
        'datas_json': datas_json,
        'velocidades_json': velocidades_json
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  
            if user is not None:
                login(request, user)  
                return redirect('meus_produtos')  
            else:
                messages.error(request, 'Usuário ou senha inválidos')
    else:
        form = LoginForm() 
    return render(request, 'login.html', {'form': form})





def register(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')
        else: 
            for field in form:
                for error in field.errors:
                    messages.error(request, "{}: {}".format(field.label, error))
            for error in form.non_field_errors():
                messages.error(request, error)
    else: 
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def detalhes_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    return render(request, 'detalhes_produto.html', {'produto': produto})

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response['Refresh'] = '5;url=' + str(reverse_lazy('login'))
        return response
    
@api_view(['POST'])
def receber_medicao(request):
    velocidade = request.data.get('velocidade')
    usuario_id = request.data.get('usuario_id')
    dispositivo_id = request.data.get('dispositivo_id')  

    if velocidade is not None and usuario_id is not None and dispositivo_id is not None:
        try:
            usuario = User.objects.get(id=usuario_id)
            medicao = MedicaoVelocidade(velocidade=velocidade, usuario=usuario, dispositivo_id=dispositivo_id)
            medicao.save()
            return Response({"status": "sucesso", "velocidade": velocidade})
        except User.DoesNotExist:
            return Response({"status": "erro", "mensagem": "Usuário não encontrado."})
    else:
        return Response({"status": "erro", "mensagem": "Dados incompletos."})




