from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetCompleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, LoginForm
from django.contrib import messages
from .models import Produto
from django.contrib.auth.decorators import login_required


@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def meus_produtos(request):
    produtos = Produto.objects.filter(usuario=request.user)
    return render(request, 'meus_produtos.html', {'produtos': produtos})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Pass request.POST to the form
        if form.is_valid():  # Check if the form is valid
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  # Authenticate the user
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('meus_produtos')  # Redirect to the products page
            else:
                messages.error(request, 'Usuário ou senha inválidos')
    else:
        form = LoginForm()  # An unbound form
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
        # Redireciona após 5 segundos (5000 milissegundos)
        response['Refresh'] = '5;url=' + str(reverse_lazy('login'))
        return response