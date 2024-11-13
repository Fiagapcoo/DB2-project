from cryptography.fernet import Fernet
from decouple import config

def load_key():
    """
    Loads the Fernet key from an environment variable.
    """
    key = config('FERNET_TOKEN')
    return key.encode()  # Ensure the key is in bytes

def encrypt_string(input_string):
    """
    Encrypts a string and returns the encrypted data.
    """
    key = load_key()
    f = Fernet(key)
    
    data = input_string.encode()  # Convert string to bytes
    encrypted_data = f.encrypt(data)
    
    return encrypted_data.decode()  # Convert bytes back to string

def decrypt_string(encrypted_string):
    """
    Decrypts an encrypted string and returns the decrypted data.
    """
    key = load_key()
    f = Fernet(key)
    
    encrypted_data = encrypted_string.encode()  # Convert string to bytes
    decrypted_data = f.decrypt(encrypted_data)
    
    return decrypted_data.decode()  # Convert bytes back to string

# Usage:
if __name__ == "__main__":
    # Example string to encrypt
    original_string = "This is a secret message."
    print(f"Original String: {original_string}")
    
    # Encrypt the string
    encrypted = encrypt_string(original_string)
    print(f"Encrypted String: {encrypted}")
    
    # Decrypt the string
    decrypted = decrypt_string(encrypted)
    print(f"Decrypted String: {decrypted}")
