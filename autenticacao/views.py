from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.db import connection
from encryption.encrypt_decrypt import encrypt_string
from django.contrib import messages

# Create your views here.

def index(request):
    return redirect('login')


def login(request):
    #check if the user is authenticated if so render the home page
    return render(request, 'login.html')



def register(request):
    print("register")
    if request.method == 'POST':
        print("register post")
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = encrypt_string(request.POST.get('email'))
            password = encrypt_string(request.POST.get('password'))
            phone_number = encrypt_string(request.POST.get('phone_number'))
            full_name = f"{first_name} {last_name}"

            with connection.cursor() as cursor:
                cursor.execute("CALL HR.InsertUser(%s, %s, %s, %s)", [full_name, phone_number, email, password])

            messages.success(request, "Account created successfully!")

        except Exception as e:
            messages.error(request, f"Error creating account: {e}")

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