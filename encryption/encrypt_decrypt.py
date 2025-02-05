import hashlib


def encrypt_string(input_string):
    """
    Converte uma string em um hash SHA-256 irreversível.
    """
    hashed_string = hashlib.sha256(input_string.encode()).hexdigest()
    return hashed_string


