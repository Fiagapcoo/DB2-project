from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.db import connection
from encryption.encrypt_decrypt import encrypt_string, decrypt_string
from django.contrib import messages
from cryptography.fernet import InvalidToken

# Create your views here.

def index(request):
    return redirect('login')


def login(request):
    if request.method == 'POST':
        input_email = request.POST.get('email')
        input_password = request.POST.get('password')
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT UserID, Name, Email, HashedPassword FROM HR.Users")
            users = cursor.fetchall()
            
            for user in users:
                try:
                    user_id, user_name, encrypted_email, encrypted_password = user
                    
                    decrypted_email = decrypt_string(encrypted_email)
                    decrypted_password = decrypt_string(encrypted_password)
                    
                    print(f"Decrypted Email: {decrypted_email}")
                    print(f"Decrypted Password: {decrypted_password}")
                    
                    if decrypted_email == input_email and decrypted_password == input_password:

                        request.session['user_id'] = user_id
                        request.session['user_name'] = user_name
                        return redirect('home') #go to store page
                except InvalidToken:
                    print("Error: Decryption failed for a user record. Skipping this record.")
                    continue
            
            messages.error(request, 'Credenciais inválidas.')
                
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