import base64
import hashlib
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256


def aes_rsa_convert(text, action, public_key=None, private_key=None):
    """
    Hybrid AES-256 + RSA-OAEP(SHA-256).
    Encrypt: uses RSA public key to wrap a random AES key; returns Base64(JSON).
    Decrypt: uses RSA private key to unwrap and decrypt the ciphertext.

    Args:
        text (str): plaintext (encrypt) or Base64(JSON) package (decrypt)
        action (str): 'encrypt' or 'decrypt'
        public_key (str): PEM public key (required for encrypt)
        private_key (str): PEM private key (required for decrypt)

    Returns:
        str: ciphertext package (encrypt) or plaintext (decrypt)
    """
    if action == 'encrypt':
        if not public_key:
            raise ValueError('RSA public key is required for AES-RSA encryption.')

        # RSA setup (OAEP with SHA-256)
        rsa_key = RSA.import_key(public_key)
        rsa_cipher = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA256)

        # Random AES-256 key + IV
        aes_key = get_random_bytes(32)
        iv = get_random_bytes(16)

        # AES-256-CBC encrypt
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))

        # Wrap AES key with RSA-OAEP
        ek_bytes = rsa_cipher.encrypt(aes_key)

        package = {
            'alg': 'AES-256-CBC+RSA-OAEP',
            'iv': base64.b64encode(iv).decode('utf-8'),
            'ek': base64.b64encode(ek_bytes).decode('utf-8'),
            'ct': base64.b64encode(ct_bytes).decode('utf-8'),
        }
        # Return as Base64(JSON) so it's a single opaque string
        return base64.b64encode(json.dumps(package).encode('utf-8')).decode('utf-8')

    elif action == 'decrypt':
        if not private_key:
            raise ValueError('RSA private key is required for AES-RSA decryption.')

        rsa_key = RSA.import_key(private_key)
        rsa_cipher = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA256)

        # Decode Base64 → JSON → fields
        try:
            package_json = base64.b64decode(text)
            package = json.loads(package_json.decode('utf-8'))
            iv = base64.b64decode(package['iv'])
            ek_bytes = base64.b64decode(package['ek'])
            ct_bytes = base64.b64decode(package['ct'])
        except Exception:
            raise ValueError('Invalid AES-RSA package format.')

        # Unwrap AES key + decrypt
        aes_key = rsa_cipher.decrypt(ek_bytes)
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct_bytes), AES.block_size).decode('utf-8')
        return pt

    return None


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
