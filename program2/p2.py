#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import math
import numpy.random as rand
from termcolor import colored, cprint


def create_key(m):
    flag = True
    while flag:
        source_seq = rand.randint(0, 2, m)

        if sum(source_seq) == 0:
            flag = True
        else: flag = False

    with open('key.txt', 'w') as f:
        for i in ''.join(str(i) for i in source_seq):
            f.write(str(i))

    return list(source_seq)


def m_seq(n, key='key.txt'):
    source_seq = []
    for char in open(key, 'r').read():
        source_seq.append(int(char))
    seq_m = [0 for k in range(n)]
    # print(''.join(str(i) for i in source_seq))

    for j in range(n):

        x = source_seq[len(source_seq)-1] ^ source_seq[2]
        seq_m[j] = source_seq[len(source_seq)-1]

        for i in range(len(source_seq)-1, 0, -1):
            source_seq[i] = source_seq[i-1]
        source_seq[0] = x

    # print(''.join(str(i) for i in seq_m))
    # print(seq_m)
    return seq_m


def serial_test(m_seq, ser, key):
    seq_m = m_seq
    dict_ser = {}
    for i in range(len(key)*2, len(seq_m)-ser+1, ser):
        a = ''
        for j in range(0, ser):
            a += str(seq_m[i+j])

        if a not in dict_ser.keys():
            dict_ser.update({a: 1})
        else:
            dict_ser.update({a:dict_ser[a]+1})
    # print(seq_m)
    # print(dict_ser)
    nt=len(seq_m) / (ser * pow(2,ser))
    ksi=0
    temp=list(dict_ser.values())

    for k in range(0, pow(2, ser)):
        ksi+=pow(temp[k]-nt, 2) / nt

    if ser == 2:
        if ksi >= 0.584 and ksi <= 6.251:
            print(colored('Серия из 2. Успешно: ','green'), end='')
            cprint(ksi, 'red', 'on_white')
        else:
            print(colored('Серия из 2. Неудача: ','red'), end='')
            cprint(ksi, 'red', 'on_white')
    elif ser == 3:
        if ksi >= 2.833 and ksi <= 12.017:
            print(colored('Серия из 3. Успешно: ','green'), end='')
            cprint(ksi, 'red', 'on_white')
        else:
            print(colored('Серия из 3. Неудача: ','red'), end='')
            cprint(ksi, 'red', 'on_white')
    elif ser == 4:
        if ksi >= 8.547 and ksi <= 22.307:
            print(colored('Серия из 4. Успешно: ','green'), end='')
            cprint(ksi, 'red', 'on_white')
        else:
            print(colored('Серия из 4. Неудача: ','red'), end='')
            cprint(ksi, 'red', 'on_white')
    else: print('Неверное значение серии')


def cor_test(m_seq, k):
    seq_m = m_seq
    x = []
    y = []
    sumXY = 0
    sumX2 = 0
    sumY2 = 0
    sX = 0
    sY = 0
    N = len(seq_m) - k

    for i in range(0, N):
        x.append(seq_m[i])
        y.append(seq_m[i+k])
        sX += x[i]
        sY += y[i]
        sumXY += x[i] * y[i]
        sumX2 += pow(x[i], 2)
        sumY2 += pow(y[i], 2)

    r = ((N * sumXY) - (sX * sY)) / \
        math.sqrt((N * sumX2 - pow(sX, 2)) * (N * sumY2 - pow(sY, 2)))

    rT = math.sqrt(N * (N - 3) / (N + 1)) * 2 / (N - 2) + 1 / (N - 1)

    if r <= rT:
        print(colored('Удача k=', 'green'), end='')
        cprint(k, 'green')
    else:
        print(colored('Неудача k=', 'red'), end='')
        cprint(k, 'red')
    print('     Практическое значение: ', end='')
    cprint(r, 'red', 'on_white')
    print(colored('     Теоретическое значение: ', ), end='')
    cprint(rT, 'red', 'on_white')


def encrypted_file():
    with open('Variant_19.txt', 'rb') as in_f:
        in_f.seek(0)
        first_bytes = in_f.read()
        in_f.close()

        source_text = []
        for i in first_bytes:
            t = bin(i)[2:]
            while len(t) != 8:
                t = '0' + t
            source_text.append(t)

        source_text = ''.join(source_text)
        seq_m = m_seq(len(source_text))


        output_arr = [0 for k in range(len(source_text))]
        for i in range(0, len(source_text)):
            output_arr[i] = int(source_text[i]) ^ int(seq_m[i])

        output_arr = ''.join(str(i) for i in output_arr)

        with open('encoded.txt', 'wb') as out_f:
            k = 0
            for j in range(0, len(output_arr), 8):
                k +=8
                temp = int(output_arr[j:k], 2)
                out_f.write(bytes([temp]))
        out_f.close()



def decrypted_file():
    with open('encoded.txt', 'rb') as in_f:
        in_f.seek(0)
        first_bytes = in_f.read()
        in_f.close()

        source_text = []
        for i in first_bytes:
            t = bin(i)[2:]
            while len(t) != 8:
                t = '0' + t
            source_text.append(t)

        source_text = ''.join(source_text)
        seq_m = m_seq(len(source_text))

        output_arr = [0 for k in range(len(source_text))]
        for i in range(0, len(source_text)):
            output_arr[i] = int(source_text[i]) ^ int(seq_m[i])

        output_arr = ''.join(str(i) for i in output_arr)

        with open('decoded.txt', 'wb') as out_f:
            k = 0
            for j in range(0, len(output_arr), 8):
                k +=8
                temp = int(output_arr[j:k], 2)
                out_f.write(bytes([temp]))
        out_f.close()
        # print(source_text)
        # print(''.join(str(i) for i in seq_m))
        # print(output_arr)


create_key(32)
f = open('key.txt', 'r').read()
key = []
key1 = [ i for i in range(0, 15)]
for i in f:
    key.append(int(i))


encrypted_file()
decrypted_file()


with open('Variant_19.txt', 'rb') as in_f:
    in_f.seek(0)
    first_bytes = in_f.read()
    in_f.close()

    source_text = []
    for i in first_bytes:
        t = bin(i)[2:]
        while len(t) != 8:
            t = '0' + t
        source_text.append(t)

t = ''
with open('encoded.txt', 'rb') as in_f:
    in_f.seek(0)
    first_bytes = in_f.read()
    in_f.close()

    encoded_text = []
    for i in first_bytes:
        t = bin(i)[2:]
        while len(t) != 8:
            t = '0' + t
        encoded_text.append(t)

source = []
for i in source_text:
    for j in range(0 ,len(i)):
        source.append(int(i[j]))

encoded = []
for i in encoded_text:
    for j in range(0 ,len(i)):
        encoded.append(int(i[j]))

ser = 3
k = 2

print('Тесты последовательности'.upper().center(70))
print()
print('Сериальный тест последовательности: ', end='')
serial_test(m_seq(70000), ser, key)
print()
print()
print('Корреляционный тест последовательности: ', end='')
cor_test(m_seq(70000), k)
print()
print('Тесты файла'.upper().center(70))
print()
print('Сериальный тест исходного файла: ', end='')
serial_test(source, ser, key)
print()
print()
print('Корреляционный тест исходного файла: ')
cor_test(source, k)
print()
print()
print('Сериальный тест зашифрованного файла: ', end='')
serial_test(encoded, ser, key)
print()
print()
print('Корреляционный тест зашифрованного файла: ')
cor_test(encoded, k)
