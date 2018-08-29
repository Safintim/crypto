#!/usr/bin/python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import random as ran
from time import time


def generate_int(n):
    simple_int = '1'
    for i in range(0, n-2):
        simple_int += str(ran.getrandbits(1))
    simple_int = simple_int + '1'
    simple_int = int(simple_int, 2)

    return simple_int


def pows(x, d, n):
    y = 1
    while d > 0:
        if d % 2 != 0:
            y = (y * x) % n

        d = d // 2
        x = (x * x) % n
    return y


def check_simple_int(sInt):
    flag = True
    for i in range(1, 101):
        if pows(i, sInt - 1, sInt) == 1:
            pass
        else: flag = False; break

    return flag


def generate_simple_int(n):
    sInt = generate_int(n)
    while not check_simple_int(sInt):
        sInt = generate_int(n)

    return sInt


def full_euclid(m, n):
    a = m
    b = n
    u1 = 1
    u2 = 0
    v1 = 0
    v2 = 1

    while b != 0:
        q = a // b
        r = a % b
        a = b
        b = r
        r = u2
        u2 = u1 - q * u2
        u1 = r
        r = v2
        v2 = v1 - q * v2
        v1 = r

    if u1 < 0:
        u1 += n

    return u1


def euclid(m, n):
    if m == 0:
        return n
    elif n == 0:
        return m
    elif m > n:
        return euclid(n, m % n)
    elif m < n:
        return euclid(n % m, n)


def create_keys(l, exp):
    p = generate_simple_int(l // 2)
    q = generate_simple_int(l // 2)
    n = p * q
    fi = (p - 1) * (q - 1)
    flag = False
    while not flag:
        if euclid(fi, exp) == 1:
            with open('public_key.txt', 'w') as f_key:
                f_key.write(str(exp) + '\n')
                f_key.write(str(n))

            d = full_euclid(exp, fi)

            with open('private_key.txt', 'w') as f_key:
                f_key.write(str(d) + '\n')
                f_key.write(str(n))
            flag = True
        else:
            print("Выберите другую экспоненту!")
            exp = int(input())


def create_keys_one_prime(l, exp, not_prime):
    p = generate_simple_int(l // 2)
    q = not_prime
    n = p * q
    fi = (p - 1) * (q - 1)
    flag = False
    while not flag:
        if euclid(fi, exp) == 1:
            with open('public_key.txt', 'w') as f_key:
                f_key.write(str(exp) + '\n')
                f_key.write(str(n))

            d = full_euclid(exp, fi)

            with open('private_key.txt', 'w') as f_key:
                f_key.write(str(d) + '\n')
                f_key.write(str(n))
            flag = True
        else:
            print("Выберите другую экспоненту!")
            exp = int(input())


def encrypted(len_key, file='INPUT.txt', public_key='public_key.txt'):
    with open(file, 'r') as in_f:
        text = in_f.read(len_key // 64)

        bytes_text = ''
        for byte in text:
            t = bin(ord(byte.encode(encoding='cp1251')))[2:]
            while len(t) != 8: # 8 b
                t = '0' + t
            bytes_text += t

    m = int(bytes_text, 2)

    with open(public_key, 'r') as pub_k:
        string = pub_k.readline()
        exp = int(string[:len(string) - 1])
        n = int(pub_k.readline())
        pub_k.close()

    c = pows(m, exp, n)
    with open('encoded.txt', 'w') as encoded:
        encoded.write(bin(c)[2:])

    return c


def decrypted(len_key, file='encoded.txt', private_key = 'private_key.txt',):
    in_f = open(file, 'r')
    temp = in_f.read()
    in_f.close()

    with open(private_key, 'r') as private_k:
        string = private_k.readline()
        d = int(string[:len(string) - 1])
        n = int(private_k.readline())

    c = int(temp, 2)
    m = pows(c, d, n)
    m = bin(m)[2:]

    while len(m) % 8 != 0: # 8 b
        m = '0' + m
    s = ''
    temp = ''
    with open('decode.txt', 'wb') as decode:
        for j in range(0, len(m), 8):
            temp = int(m[j:j+8], 2)
            decode.write(bytes([temp]))


def pollard(n):
    x = 3
    y = 1
    i = 0
    stage = 2
    while euclid(n, abs(x - y)) == 1:
        if i == stage:
            y = x
            stage = stage * 2
        x = (x * x - 1) % n
        i += 1
    d = euclid(n, abs(x - y))
    return euclid(n, abs(x - y))


# print(pollard(347595345088061083538285659))


def attack(start=30, stop=40):
    y = []
    x = []

    while start <= stop:
        p = generate_simple_int(start)
        q = generate_simple_int(start)
        n = p * q
        t1 = time()
        pollard(n)
        t2 = time() - t1
        y.append(t2)
        x.append(start * 2)
        start += 1
        if t2 < 10:
            start += 1
    else:
        return (start - 1) * 2, x, y


def paint(x, y, text_y, text_x):
    plt.plot(x, y, color='green', marker='o', ls='solid')
    plt.title('График')
    plt.ylabel(text_y)
    plt.xlabel(text_x)
    plt.show()


def diff_len_pq(l):
    r = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    y = []

    for i in r:
        p = generate_simple_int(round(i * l))
        q = generate_simple_int(round((1 - i) * l))
        n = p * q
        t1 = time()
        pollard(n)
        t2 = time() - t1
        y.append(t2)
    paint(r, y, 'время', 'r')


cort = attack()
l = cort[0]
x = cort[1]
y = cort[2]
paint(x, y, 'время', 'длина ключа')
diff_len_pq(l)

t1 = time()
len_key = 256
create_keys_one_prime(len_key, 17, 128)
create_keys(len_key, 17)
encrypted(len_key)
decrypted(len_key)
print(time() - t1)