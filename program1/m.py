#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random

ALPHABET=[' ','а','б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
  'А','Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

FILE='Variant_19.txt'
FILE_KEY='key.txt'
# PUNCTUATION=['.',',','-',';','?','!',':','(',')','"',"'", '\n']


def create_key(ALPHABET, FILE_KEY):
    alphabet_key = ALPHABET.copy()
    random.shuffle(alphabet_key)
    f=open(FILE_KEY, 'w')
    f.write(''.join(alphabet_key))
    return alphabet_key


def encrypted_file(file, dict_crypto):
    input_file = open(file, 'r')
    output_file=open(file+'_crypto', 'w')

    for char in input_file.read():
        if char in dict_crypto.keys():
            output_file.write(dict_crypto[char])
        else:
            pass

    return output_file.name


def decrypted_file(FILE_KEY, ALPHABET, ENCR_FILE):

    f=open(FILE_KEY, 'r')
    alphabet_key=[]
    for char in f.read():
        alphabet_key.append(char)
    dict_crypto = dict(zip(alphabet_key, ALPHABET))
    input_file=open(ENCR_FILE, 'r')
    output_file=open(FILE+'_decrypto', 'w')
    for char in input_file.read():
        if char in dict_crypto.keys():
            output_file.write(dict_crypto[char])
        else:
            pass


# создание ключа(key.txt) и словаря
dict_crypto = dict(zip(ALPHABET, create_key(ALPHABET, FILE_KEY)))
# шифрование файла
ENCR_FILE=encrypted_file(FILE,dict_crypto)
# ENCR_FILE='Variant_19.txt_crypto'
# расшифровка файла
decrypted_file(FILE_KEY, ALPHABET, ENCR_FILE)