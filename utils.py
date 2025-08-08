import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def base64_convert(text, action):
    """
    Encodes or decodes a string using Base64.

    Args:
        text (str): The input string.
        action (str): 'encode' or 'decode'.

    Returns:
        str: The converted string.
    """
    if action == 'encode':
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    elif action == 'decode':
        return base64.b64decode(text).decode('utf-8')
    return None

def hash_convert(text, algorithm):
    """
    Hashes a string using the specified algorithm.

    Args:
        text (str): The input string.
        algorithm (str): The hashing algorithm (e.g., 'sha256', 'md5').

    Returns:
        str: The hashed string.
    """
    hasher = hashlib.new(algorithm)
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()

def aes_convert(text, action, key):
    """
    Encrypts or decrypts a string using AES-256.

    Args:
        text (str): The input string.
        action (str): 'encrypt' or 'decrypt'.
        key (str): The encryption key.

    Returns:
        str: The converted string.
    """
    # Use a fixed-size key (32 bytes for AES-256)
    key = key.encode('utf-8')
    key = hashlib.sha256(key).digest()

    if action == 'encrypt':
        cipher = AES.new(key, AES.MODE_CBC)
        # The IV is prepended to the ciphertext
        iv = cipher.iv
        ciphertext = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
        return base64.b64encode(iv + ciphertext).decode('utf-8')
    elif action == 'decrypt':
        # The IV is the first 16 bytes of the decoded ciphertext
        decoded_text = base64.b64decode(text)
        iv = decoded_text[:16]
        ciphertext = decoded_text[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
    return None
