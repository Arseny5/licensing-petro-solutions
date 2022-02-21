# Информацию о железе можно получить через классы WMI.
# Если делать привязку, то можно пользоваться серийным номером HDD и его моделью.
# Полученные данные можно зашифровать, сохранить в файл, попросить пользователя отправить вложением по почте.
# На основе этих данных можно сгенерировать ключ, прислать его пользователю.
# При регистрации прописать в файл или в реестр.
# При запуске программы проверять его наличие.
# Если ключа нет, то программа не запускается, если ключ есть, то декодировать его, узнать железо и сравнить с установленным.

# 1. Избавиться от сетевых запросов.
# 2. Генератор лицензии -> шифрование hwid хэшированием. (OpenSSL)
# 3. Сравнение зашифроанного hwid от пользователя в лицензии с hwid на текущем пк.
# 4. Nuitka -> компилирование под плюсы
# 5. Обфусцирование -> nuitka -> сжатие


import subprocess, requests, time, os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
import uuid
import OpenSSL
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import OpenSSL.crypto as ct
import base64
from PIL import Image, ImageTk


# check hwid
hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
print("First variant: " + hwid)
hwid = str(uuid.uuid5(uuid.NAMESPACE_OID, hwid))
print("Second variant: " + hwid) # decode UUID

# check public_key from this directory
key_filename = 'rsa_public_key.pem'
key_file = open(key_filename, 'r')
key_buffer = key_file.read()
key_file.close()
public_key = ct.load_publickey(ct.FILETYPE_PEM, key_buffer)
print(key_buffer)

# Генерация файла с hwid_uuid
def generate_file_with_hwid_uuid(hwid):
    with open('hwid_to_license.txt', 'w') as tw:
        tw.write(hwid)


root = Tk()
root.geometry("800x500")
root.title("Проверка ключа активации")
root.resizable(width=False, height=False)
root.image = ImageTk.PhotoImage(Image.open("background.png"))
bg_logo = Label(root, image=root.image)
bg_logo.place(x=0, y=0, relwidth=1, relheight=1)

test = None
title = None
title1 = None
title2 = None

# generate UI with HWID
def create_first_window():
    global title
    global title1
    global title2

    title = Label(root, text="\nПроверка ключа\n\n", font="Arial 30")
    title.pack()

    title1 = Label(root, text="Ваш hwid: " + hwid)
    title1.pack()

    title2 = Label(root, text="\nОтправьте данный персональный код для получения лицензии:\n" + "На почту: petrosolutions@mail.ru\n" + "По номеру телефона: 8-903-777-77-77\n\n\n\n\n\n\n")
    title2.pack()

    generate_file_with_hwid_uuid(hwid)

    global test
    test = Button(root, text="Дальше", command=create_second_window)
    test.pack()

def create_second_window():
    global test
    global title
    global title1
    global title2
    test.destroy() # or place_forget if you want
    title.destroy()
    title1.destroy()
    title2.destroy()

    title = Label(root, text="\n\nЛол\n", font="Arial 30")
    title.pack()

    title1 = Label(root, text=hwid)
    title1.pack()

    text = Text(width=50, height=25)

    def insert_text():
        file_name = fd.askopenfilename()
        f = open(file_name)
        s = f.read()
        text.insert(1.0, s)
        f.close()

    insert_signa = Button(text="Открыть", command=insert_text)
    insert_signa.pack()

create_first_window()
root.mainloop()