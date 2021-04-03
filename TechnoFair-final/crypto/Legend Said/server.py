#!/usr/bin/python3
from secret import flag
from Crypto.Cipher import AES
import sys, binascii
from Crypto.Util.Padding import pad
from os import urandom
import random

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

class Random():
    n = random.randint(1000000000, 9999999999)
    m = random.randint(1000000000, 9999999999)
    c = random.randint(1000000000, 9999999999)

    def __init__(self, s):
        self.state = s

    def next(self):
        self.state = (self.m * self.state + self.c) % self.n
        return self.state

def encrypt_AES(key, m):
    message = pad(m, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(message)
    ciphertext = binascii.hexlify(encrypted)
    return ciphertext

def main():
    key = urandom(16)
    chance = 0
    seed = random.randint(1000000000, 9999999999)
    r = Random(seed)
    rand_values = [seed]
    for i in range(9):
        rand_values.append(r.next())

    rand_cipher = []
    for i in rand_values:
        m = str(i).encode()
        rand_cipher.append(encrypt_AES(key, m))

    while True:
        print ('''=========================================
        Menu Utama
    1. Current Random Cipher
    2. Next Random Cipher
    3. Guess Next Random Cipher
    4. Encrypt Something
    5. Panggil Dukun
    6. Exit
=========================================''')

        pilihan = input("Masukan Pilihan: ")
        print('-----------------------------------------')
        if pilihan == '1':
            print('Current Random Ciphertext: ', rand_cipher[chance])

        elif pilihan == '2':
            chance += 1
            if chance >= 9:
                print('Auu ah cape :(')
                exit()
            else:
                print('Next Random Ciphertext: ', rand_cipher[chance])

        elif pilihan == '3':
            guess = input('Masukkan Prediksi Next Cipher: ')
            guess = guess.encode()
            if guess == rand_cipher[chance+1]:
                print('=========== CONGRATSSS ============')
                print('this is your flag:', flag)
                exit()
            else:
                print('Salah bwangg')

        elif pilihan == '4':
            message = str(input('Plaintext: '))
            cipher = encrypt_AES(key, message.encode())
            print('Ciphertext: ', cipher)

        elif pilihan == '5':
            print('Dukun will help you with the current random cipher')
            message = input('Pesan untuk dukun: ')
            cipher = encrypt_AES(key, (message+str(rand_values[chance])).encode())
            print('Balasan dari dukun: ', cipher)

        elif pilihan == '6':
            print('Babayy ~~~~')
            exit()

        else:
            print(">:(")
            exit()

if __name__ == "__main__":
    main()
