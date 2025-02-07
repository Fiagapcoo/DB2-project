import hashlib
import random
import string


def encrypt_string(input_string):
    """
    Converte uma string em um hash SHA-256 irreversível.
    """
    hashed_string = hashlib.sha256(input_string.encode()).hexdigest()
    return hashed_string


def gerar_string_aleatoria():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(100))

def gerar_segredo():

    codigo = gerar_string_aleatoria()
    return encrypt_string(codigo)
