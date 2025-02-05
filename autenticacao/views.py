from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from encryption.encrypt_decrypt import encrypt_string
from django.contrib import messages
from cryptography.fernet import InvalidToken
from email_handler.email import gerar_codigo_recuperacao,enviar_email_recuperacao
from django.http import JsonResponse

# Create your views here.

def index(request):
    if request.session.get('user_id'):
        return redirect('http://127.0.0.1:8000/store')

    return redirect('login')


def login(request):
    if request.session.get('user_id'):
        return redirect('http://127.0.0.1:8000/store')
    
    if request.method == 'POST':
        input_email = request.POST.get('email')
        input_password = request.POST.get('password')

        if not input_email or not input_password:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'login.html')

        try:
            with connection.cursor() as cursor:
                # Use parameterized queries to prevent SQL injection
                cursor.execute(
                    "SELECT UserID, Name, Email, HashedPassword FROM HR.Users WHERE Email = %s",
                    [input_email]
                )
                user = cursor.fetchone()

            if user is None:
                messages.error(request, 'Credenciais inválidas.')
                return render(request, 'login.html')

            user_id, name, email, hashed_password = user

            try:
                # Encript and compare to password
                comparador = encrypt_string(input_password)
                if hashed_password == comparador:
                    # Store user details in the session
                    request.session['user_id'] = user_id
                    request.session['user_name'] = name
                    request.session['user_email'] = email
                    return redirect('index')

            except InvalidToken:
                messages.error(request, 'Ocorreu um erro ao processar as suas credenciais.')

        except Exception as e:
            # Log exception and notify the user (ensure to log securely in production)
            print(f"Error during login: {e}")
            messages.error(request, 'Erro interno. Por favor, tente novamente mais tarde.')


    return render(request, 'login.html')


def register(request):
    context = {
        "registration_success": False,
        "registration_error": False
    }

    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = encrypt_string(request.POST.get('password'))  # Assuming this function is defined
            phone_number = request.POST.get('phone_number')
            full_name = f"{first_name} {last_name}"
            is_manager = False

            print("full_name: ", full_name)
            print("phone_number: ", phone_number)
            print("email: ", email)
            print("password: ", password)

            with connection.cursor() as cursor:
                # Explicitly pass the is_manager parameter
                cursor.execute("CALL HR.InsertUser(%s, %s, %s, %s, %s)", 
                               [full_name, phone_number, email, password, is_manager])

                messages.success(request, 'Conta criada com sucesso')
                return redirect("index")  # Redirect only after successful registration

        except Exception as e:
            context["registration_success"] = False  # Ensure success is False
            context["registration_error"] = True     # Set error flag
            context["error_message"] = str(e)        # Store error message for debugging
            messages.error(request, f"Erro ao criar conta: {str(e)}")  # Display error message

    return render(request, 'register.html', context)


def password_recovery(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        if not email:
            return JsonResponse({"success": False, "error": "Email é obrigatório"}, status=400)
        
        with connection.cursor() as cursor:
            cursor.execute('''
            SELECT u.userid FROM hr.users u 
            WHERE u.email = %s
        ''',[email])
        
        row = cursor.fetchone()

        if not row:
            return JsonResponse({"sucess": False, "error" : "Este email não está registado" }, status=400)
        
        user_id = row[0]

        # Geração e envio do código
        codigo = gerar_codigo_recuperacao()
        
        cursor.execute('''
                DELETE FROM CONTROL.codigos_recuperacao
                WHERE userid = %s
        ''',[user_id])
    
        enviar_email_recuperacao(email, codigo)

        cursor.execute('''
                 INSERT INTO CONTROL.codigos_recuperacao (userid, criacao, codigo)
                 VALUES (%s, NOW(), %s)
             ''', [user_id, codigo])
      
      
        return JsonResponse({"success": True})

    # Para GET, renderiza o template
    return render(request, "password_recovery.html")

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

