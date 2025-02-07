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

    html_content = f"""
    <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    
    <table role="presentation" width="100%" max-width="600px" border="0" cellspacing="0" cellpadding="0" style="margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <tr>
            <td style="padding: 40px 30px;">
                <h1 style="color: #333333; font-size: 24px; margin: 0 0 20px; text-align: center;">Recuperação da Palavra-passe</h1>
                
                <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0 0 20px;">
                    Olá,
                </p>
                
                <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0 0 20px;">
                    Recebemos um pedido para redefinir a sua palavra-passe. Utilize o código de verificação abaixo para concluir o processo:
                </p>
                
                <div style="background-color: #f8f9fa; border-radius: 4px; padding: 20px; margin: 30px 0; text-align: center;">
                    <span style="font-family: 'Courier New', monospace; font-size: 32px; font-weight: bold; color: #333333; letter-spacing: 5px;">
                        {codigo_recuperacao}
                    </span>
                </div>
                
                <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0 0 20px;">
                    Este código expirará em 15 minutos por motivos de segurança. Se não solicitou esta redefinição de palavra-passe, por favor ignore este email.
                </p>
                
                <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0 0 20px;">
                    Para sua segurança, nunca partilhe este código com ninguém.
                </p>
                
                <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 30px 0 0;">
                    Com os melhores cumprimentos,<br>
                    A Equipa da Tetris micescrnfmice
                </p>
            </td>
        </tr>
    </table>
    
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
        <tr>
            <td style="padding: 30px 30px; text-align: center;">
                <p style="color: #999999; font-size: 14px; margin: 0;">
                    Esta é uma mensagem automática, por favor não responda a este email.<br>
                    © 2025 Tetris micescrnfmice. Todos os direitos reservados.
                </p>
            </td>
        </tr>
    </table>
</body>
</html>
    """
    send_smtp_email = SendSmtpEmail(
        to=[{"email": email_destino, "name": "Destinatário"}],
        sender={"email": "rafafern04.pint@gmail.com", "name": "BD2"},
        subject="Recuperação da Palavra-passe",
        text_content="Recuperação de Senha",
        html_content=html_content
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
    
    html_content = f"""
    <!DOCTYPE html>
<html>
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
   
   <table role="presentation" width="100%" max-width="600px" border="0" cellspacing="0" cellpadding="0" style="margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
       <tr>
           <td style="padding: 40px 30px;">
               <h1 style="color: #333333; font-size: 24px; margin: 0 0 20px; text-align: center;">Bem-vindo(a) à Nossa Loja de Instrumentos! 🎵</h1>
               
               <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0 0 20px;">
                   Olá {nome},
               </p>
               
               <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0 0 20px;">
                   É com grande satisfação que lhe damos as boas-vindas à nossa loja de instrumentos musicais. Estamos muito contentes por tê-lo(a) connosco!
               </p>
               
               <div style="background-color: #f8f9fa; border-radius: 4px; padding: 20px; margin: 30px 0;">
                   <h2 style="color: #333333; font-size: 18px; margin: 0 0 15px;">O que pode encontrar na nossa loja:</h2>
                   <ul style="color: #666666; font-size: 16px; line-height: 24px; margin: 0; padding-left: 20px;">
                       <li>Uma vasta seleção de instrumentos musicais de qualidade</li>
                       <li>Acessórios e equipamentos profissionais</li>
                       <li>Preços competitivos</li>
                   </ul>
               </div>
               
               <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0 0 20px;">
                   A nossa equipa está sempre disponível para o(a) ajudar com qualquer questão ou dúvida que possa ter. Não hesite em contactar-nos!
               </p>
               
               <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0 0 20px;">
                   Desejamos-lhe excelentes compras e muita música! 🎸🥁🎹
               </p>
               
               <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 30px 0 0;">
                   Com os melhores cumprimentos,<br>
                   A Equipa da Tetris micescrnfmice
               </p>
           </td>
       </tr>
   </table>
   
   <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
       <tr>
           <td style="padding: 30px 30px; text-align: center;">
               <p style="color: #999999; font-size: 14px; margin: 0;">
                   © 2025 Tetris micescrnfmice. Todos os direitos reservados.
               </p>
           </td>
       </tr>
   </table>
</body>
</html>
    """

    send_smtp_email = SendSmtpEmail(
    to=[{"email": email_destino, "name": "Destinatário"}],
    sender={"email": "rafafern04.pint@gmail.com", "name": "BD2"},
    subject="Bem-vindo à nossa loja de instrumentos! 🎶",
    text_content="Email de boas Vindas",
    html_content=html_content
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Email enviado com sucesso!")
        print("Resposta da API:", api_response)
    except ApiException as e:
        print("Erro ao enviar email:", e)
    

