import os
import random
from dotenv import load_dotenv

from sib_api_v3_sdk import ApiClient, Configuration
from sib_api_v3_sdk.api.transactional_emails_api import TransactionalEmailsApi
from sib_api_v3_sdk.models.send_smtp_email import SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException

load_dotenv()



def gerar_codigo_recuperacao():
    """Gera um código aleatório de 6 dígitos para recuperação de senha."""
    return str(random.randint(100000, 999999))

def enviar_email_recuperacao(email_destino, codigo_recuperacao):
    """Envia um e-mail com o código de recuperação para o usuário."""

    brevo_api_key = os.getenv("BREVO_API_KEY")

    configuration = Configuration()
    configuration.api_key['api-key'] = brevo_api_key

    # Cria o cliente da API sem usar 'with'
    api_client = ApiClient(configuration)

    # Instancia a API de e-mails transacionais
    api_instance = TransactionalEmailsApi(api_client)

    # Configura a mensagem que será enviada
    send_smtp_email = SendSmtpEmail(
        to=[{"email": email_destino, "name": "Destinatário"}],
        sender={"email": "rafafern04.pint@gmail.com", "name": "BD2"},
        subject="Recuperçao de email",
        text_content="Recuperação de Senha",
        html_content=f"<h1>Recuperação de senha</h1><br><h2>CODIGO: {codigo_recuperacao}</h2>"
    )
    
    try:
      
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Email enviado com sucesso!")
        print("Resposta da API:", api_response)
    except ApiException as e:
        print("Erro ao enviar email:", e)


def enviar_email_boas_vindas(email_destino,nome):
        
        
    brevo_api_key = os.getenv("BREVO_API_KEY")
    configuration = Configuration()
    configuration.api_key['api-key'] = brevo_api_key

    api_client = ApiClient(configuration)

    api_instance = TransactionalEmailsApi(api_client)

    send_smtp_email = SendSmtpEmail(
    to=[{"email": email_destino, "name": "Destinatário"}],
    sender={"email": "rafafern04.pint@gmail.com", "name": "BD2"},
    subject="Bem-vindo à nossa loja de instrumentos! 🎶",
    text_content="Email de boas Vindas",
    html_content=f"<h1>Olá {nome},</h1><br><h3>Obrigado por se registrar na nossa loja de instrumentos! Aqui, você encontrará tudo o que precisa para a sua jornada musical.</h3><br><h3>Se tiver alguma dúvida, estamos à disposição para ajudar.</h3><br><h3>Bons sons e boas compras! 🎸🥁🎹</h3><h3>Atenciosamente, Tetris micescrnfmice</h3>"
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Email enviado com sucesso!")
        print("Resposta da API:", api_response)
    except ApiException as e:
        print("Erro ao enviar email:", e)
    

