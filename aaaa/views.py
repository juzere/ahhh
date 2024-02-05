from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetCompleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, LoginForm
from django.contrib import messages
from .models import Produto
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MedicaoVelocidade
from django.contrib.auth.decorators import login_required


@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def meus_produtos(request):
    produtos = Produto.objects.filter(usuario=request.user)
    medicoes = MedicaoVelocidade.objects.all().order_by('-data_hora')[:3]  
    return render(request, 'meus_produtos.html', {'produtos': produtos, 'medicoes': medicoes})


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
    if velocidade is not None:
        medicao = MedicaoVelocidade(velocidade=velocidade)
        medicao.save()
        return Response({"status": "sucesso", "velocidade": velocidade})
    else:
        return Response({"status": "erro", "mensagem": "Velocidade não fornecida."})

from django.shortcuts import render
from .models import MedicaoVelocidade



