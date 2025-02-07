from django.shortcuts import render, redirect
from .models import *
from django.db import connection
from encryption.encrypt_decrypt import encrypt_string
from django.contrib import messages
from cryptography.fernet import InvalidToken
from email_handler.email import gerar_codigo_recuperacao,enviar_email_recuperacao,enviar_email_boas_vindas
from django.http import JsonResponse
import json
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta



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

                cursor.execute(
                    "SELECT * FROM HR.get_user_details_by_email(%s);",
                    [input_email]
                )
                user = cursor.fetchone()

            if user is None:
                messages.error(request, 'Credenciais inválidas.')
                return render(request, 'login.html')

            user_id, name, email, hashed_password = user

            try:
 
                comparador = encrypt_string(input_password)
                if hashed_password == comparador:

                    request.session['user_id'] = user_id
                    request.session['user_name'] = name
                    request.session['user_email'] = email
                    return redirect('index')

            except InvalidToken:
                messages.error(request, 'Ocorreu um erro ao processar as suas credenciais.')

        except Exception as e:
           
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
            password = encrypt_string(request.POST.get('password')) 
            phone_number = request.POST.get('phone_number')
            full_name = f"{first_name} {last_name}"
            is_manager = False

            print("full_name: ", full_name)
            print("phone_number: ", phone_number)
            print("email: ", email)
            print("password: ", password)

            with connection.cursor() as cursor:

                cursor.execute("CALL HR.InsertUser(%s, %s, %s, %s, %s)", 
                               [full_name, phone_number, email, password, is_manager])

                messages.success(request, 'Conta criada com sucesso')
                enviar_email_boas_vindas(email,full_name)
                return redirect("index")

        except Exception as e:
            context["registration_success"] = False
            context["registration_error"] = True
            context["error_message"] = str(e)
            messages.error(request, f"Erro ao criar conta: {str(e)}")

    return render(request, 'register.html', context)



def password_recovery(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip()
        except json.JSONDecodeError:

            return JsonResponse({"success": False, "message": "Requisição inválida."}, status=400)

        if not email:
            return JsonResponse({"success": False, "message": "Nenhum email foi fornecido."}, status=400)


        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT HR.get_userid_by_email(%s);
            ''', [email])
            row = cursor.fetchone()

        if not row:

            return JsonResponse({
                "success": False,
                "message": "Esse email não existe na nossa base de dados."
            }, status=404)

        user_id = row[0]


        codigo = gerar_codigo_recuperacao()
        with connection.cursor() as cursor:

            cursor.execute('SELECT CONTROL.delete_codigos_recuperacao(%s)', [user_id])

            enviar_email_recuperacao(email, codigo)

            cursor.execute('''
                SELECT CONTROL.insert_codigo_recuperacao(%s,%s)
            ''', [user_id, codigo])


        request.session["reset_email"] = email


        return JsonResponse({
            "success": True,
            "message": "OTP enviado com sucesso para o seu email."
        })


    return render(request, "password_recovery.html")



def send_otp(request):
    if request.method == "GET":
        email = request.GET.get("email", "")
        return render(request, "otp.html", {"email": email})

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("otp", "")
            email = data.get("email", "").strip()
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "JSON inválido."}, status=400)

        if not email or not code:
            return JsonResponse({"success": False, "message": "Email ou código não fornecidos."}, status=400)

        try:
            code_int = int(code)
        except ValueError:
            return JsonResponse({"success": False, "message": "Código inválido (não numérico)."}, status=400)

        with connection.cursor() as cursor:
 
            cursor.execute('''
                SELECT UserID 
                FROM hr.users
                WHERE email = %s
            ''', [email])
            row_user = cursor.fetchone()

            if not row_user:
                return JsonResponse({"success": False, "message": "Utilizador não encontrado."}, status=404)

            user_id = row_user[0]


            cursor.execute('''
                SELECT criacao, codigo
                FROM control.codigos_recuperacao
                WHERE userid = %s
                ORDER BY criacao DESC
                LIMIT 1
            ''', [user_id])
            row_code = cursor.fetchone()

        if not row_code:
            return JsonResponse({"success": False, "message": "Não foi encontrado código para este utilizador."}, status=404)

        criacao_db, codigo_db = row_code


        if codigo_db != code_int:
            return JsonResponse({"success": False, "message": "Código inválido."}, status=400)


        if criacao_db.tzinfo is None:
            criacao_db = timezone.make_aware(criacao_db, timezone.get_current_timezone())


        diferenca_tempo = timezone.now() - criacao_db
        if diferenca_tempo > timedelta(minutes=5):
            return JsonResponse({"success": False, "message": "Código expirado (mais de 5 minutos)."}, status=400)

        request.session["reset_email"] = email

        return JsonResponse({"success": True, "message": "OTP validado com sucesso!"})

    return JsonResponse({"success": False, "message": "Método não suportado."}, status=405)


def reset_password(request):
    if request.method == "POST":

        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        email = request.GET.get('email', '').strip()

        if not email:
            return JsonResponse({"success": False, "error": "Email não informado."}, status=400)

        if new_password != confirm_password:
            return JsonResponse({"success": False, "error": "As senhas não coincidem."}, status=400)
        
        hashed_password = encrypt_string(new_password)
        
        with connection.cursor() as cursor:
            cursor.execute('''
               select * from "security".user_passwords_dictionary upd where hashedpassword = %s
            ''', [hashed_password])
            row = cursor.fetchone()
            if row:
                return JsonResponse({"success": False, "error": "Senha não pode ser repetida."}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE hr.users
                SET hashedpassword = %s
                WHERE email = %s
            """, [hashed_password, email])

        return JsonResponse({"success": True, "message": "Password alterada com sucesso!"})


    email = request.GET.get('email', '')
    return render(request, "reset_password.html", {"email": email})
    