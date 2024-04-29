import string
import random


class VernamCipher:
    def key_generator(plain_text):
        key = ''.join(random.choices(string.ascii_letters +
                      string.digits, k=len(plain_text)))
        return key

    def encrypt(plain_text, key):
        cipher_text = ""
        for i in range(len(plain_text)):
            num = ord(plain_text[i]) ^ ord(key[i])
            cipher_text += chr(num)
        return cipher_text

    def decrypt(cipher_text, key):
        plain_text = ""
        for i in range(len(cipher_text)):
            num = ord(cipher_text[i]) ^ ord(key[i])
            plain_text += chr(num)
        return plain_text
