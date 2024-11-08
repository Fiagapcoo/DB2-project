from django.shortcuts import render, HttpResponse, redirect
from .models import *
# Create your views here.

def index(request):
    #check if the user is authenticated if so render the home page
    return redirect('login')


def login(request):
    #check if the user is authenticated if so render the home page
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def password_recovery(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Aqui você implementaria a lógica de envio de email com OTP
        return render(request, 'password_recovery.html')
    return render(request, 'password_recovery.html')

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, 'As senhas não correspondem.')
            return render(request, 'reset_password.html')
        
        # Aqui você implementaria a lógica de atualização da senha
        messages.success(request, 'Senha atualizada com sucesso!')
        return redirect('login')
    
    return render(request, 'reset_password.html')