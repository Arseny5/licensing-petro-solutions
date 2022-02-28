timport subprocess, requests, time, os
from tkinter import *
from tkinter import messagebox
import uuid
import OpenSSL
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import OpenSSL.crypto as ct
import base64


# generate private key & write to disk
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=1024,
    backend=default_backend()
)
private_key_code = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
# generate public key
public_key = private_key.public_key()
public_key_code = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
print(private_key_code.decode(), "\n", public_key_code.decode(), "\n")

# Запись публичного ключа в файл, который далее отправим вместе с программой
with open('rsa_public_key.pem', 'w') as tw:
    tw.write(public_key_code.decode())


# Принятие от юзера его hwid. Запись в переменную
f = open("hwid_to_license.txt")
hwid_uuid = f.read()
f.close()
print(hwid_uuid)
print(" ")

# Генерация сигнатуры
def get_signa(content):
    prkey = ct.load_privatekey(ct.FILETYPE_PEM, private_key_code.decode())
    if prkey:
        signature = ct.sign(prkey, content.encode('utf8'), 'sha1')
        return signature
signa = get_signa(hwid_uuid)
print("signa: ")
print(signa)

# генерация лицензии
def get_sig(content):
    """
    Создать подпись
    :param content:
    :return:
    """
    if not content:
        return False
    pkey = ct.load_privatekey(ct.FILETYPE_PEM, private_key_code.decode())
    if pkey:
        signature = ct.sign(pkey, content.encode('utf8'), 'sha1')
        ret = base64.encodebytes(signature)
        return ret
    return False

encode_msg = get_sig(hwid_uuid)
print(" ")
print("encode_msg: ")
print(encode_msg)
print(" ")

publickey = ct.load_publickey(ct.FILETYPE_PEM, public_key_code.decode())
x509 = ct.X509()
x509.set_pubkey(publickey)

message = "lol"
print(message.encode('utf8'))
print(hwid_uuid.encode('utf8'))
print(ct.verify(x509, signa, message.encode('utf8'), 'sha1'))

print(" ")

# def encrypt_private_key(a_message, private_key): #шифрация сообщения
#     encryptor = PKCS1_OAEP.new(private_key)
#     encrypted_msg = encryptor.encrypt(a_message)
#     encoded_encrypted_msg = base64.b64encode(encrypted_msg)
#     return encoded_encrypted_msg
#
# def decrypt_public_key(encoded_encrypted_msg, public_key): #расшифровка
#     encryptor = PKCS1_OAEP.new(public_key)
#     decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
#     decoded_decrypted_msg = encryptor.decrypt(decoded_encrypted_msg)
#     #return decoded_decrypted_msg
#
# def main():
#   private, public = generate_keys()
#   print (private)
#   message = b'Hello world'
#   encoded = encrypt_private_key(message, public)
#   decrypt_public_key(encoded, private)
