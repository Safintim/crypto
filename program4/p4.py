from struct import pack
from random import randint
import matplotlib.pyplot as plt


def leftrotate(n, s):
    return ((n << s) | ((n & 0xffffffff) >> (32 - s))) & 0xffffffff


def f(x, y, z):
    return (x & y) | ((~x) & z)


def g(x, y, z):
    return (x & y) | (x & z) | (y & z)


def h(x, y, z):
    return x ^ y ^ z


def r1(a, b, c, d, k, s, x):
    return leftrotate(a + f(b, c, d) + int(x[k], 2), s)


def r2(a, b, c, d, k, s, x):
    return leftrotate((a + g(b, c, d) + int(x[k], 2) + 0x5A827999), s)


def r3(a, b, c, d, k, s, x):
    return leftrotate(a + h(b, c, d) + int(x[k], 2) + 0x6ED9EBA1, s)


def int_to_bin(a, b, c, d):
    a = bin(a)[2:]
    b = bin(b)[2:]
    c = bin(c)[2:]
    d = bin(d)[2:]
    while len(a) % 8 != 0 or len(b) % 8 != 0 or len(c) % 8 != 0 or len(d) % 8 != 0:
        if len(a) % 8 != 0:
            a = '0' + a
        elif len(b) % 8 != 0:
            b = '0' + b
        elif len(c) % 8 != 0:
            c = '0' + c
        elif len(d) % 8 != 0:
            d = '0' + d

    a = [int(x) for x in a]
    b = [int(x) for x in b]
    c = [int(x) for x in c]
    d = [int(x) for x in d]

    return a + b + c + d


def change_random_bit(msg):
    mod_msg = ''
    for char in msg:
        temp = bin(ord(char))[2:]
        while len(temp) != 8:
            temp = '0' + temp
        mod_msg += temp

    r_bit = randint(0, len(mod_msg) - 1)

    mod_msg = [x for x in mod_msg]
    mod_msg[r_bit] = str(int(mod_msg[r_bit]) ^ 1)
    mod_msg = ''.join(mod_msg)

    temp = ''
    for j in range(0, len(mod_msg), 8):
        temp += chr(int(mod_msg[j:j + 8], 2))
    mod_msg = temp
    return mod_msg


def paint(x, y, text_y, text_x):
    plt.plot(x, y, color='green', marker='o', ls='solid')
    plt.title('График')
    plt.ylabel(text_y)
    plt.xlabel(text_x)
    plt.show()


class md4(object):
    def __init__(self):
        self.A = 0x67452301
        self.B = 0xefcdab89
        self.C = 0x98badcfe
        self.D = 0x10325476
        self.result = ''
        self.X = []
        self.m = ''

    def expand_message(self, msg):

        for char in msg:
            temp = bin(ord(char))[2:]
            while len(temp) != 8:
                temp = '0' + temp
            self.m += temp

        b64 = bin(len(self.m))[2:]
        while len(b64) != 64:
            b64 = '0' + b64

        if len(self.m) % 512 == 0 & len(self.m) != 0:
            pass
        else:
            self.m += '1'
            while len(self.m) % 512 != 0:
                while len(self.m) % 512 != 448:
                    self.m += '0'
                c = b64[56:64] + b64[48:56]+b64[40:48]+b64[32:40]+b64[24:32]+b64[16:24]+b64[8:16]+b64[0:8]
                self.m += c

        for i in range(0, len(self.m), 32):
            temp = self.m[i:i+32]
            word = ''
            for j in range(0, 33, 8):
                word += temp[24-j:32-j]
            self.X.append(word)

    def rounds_f(self):

        for i in range(0, len(self.X) // 16):
            a = self.A
            b = self.B
            c = self.C
            d = self.D
            x = self.X

            # первый раунд
            a = r1(a, b, c, d, (i * 16) + 0, 3, x)
            d = r1(d, a, b, c, (i * 16) + 1, 7, x)
            c = r1(c, d, a, b, (i * 16) + 2, 11, x)
            b = r1(b, c, d, a, (i * 16) + 3, 19, x)
            a = r1(a, b, c, d, (i * 16) + 4, 3, x)
            d = r1(d, a, b, c, (i * 16) + 5, 7, x)
            c = r1(c, d, a, b, (i * 16) + 6, 11, x)
            b = r1(b, c, d, a, (i * 16) + 7, 19, x)
            a = r1(a, b, c, d, (i * 16) + 8, 3, x)
            d = r1(d, a, b, c, (i * 16) + 9, 7, x)
            c = r1(c, d, a, b, (i * 16) + 10, 11, x)
            b = r1(b, c, d, a, (i * 16) + 11, 19, x)
            a = r1(a, b, c, d, (i * 16) + 12, 3, x)
            d = r1(d, a, b, c, (i * 16) + 13, 7, x)
            c = r1(c, d, a, b, (i * 16) + 14, 11, x)
            b = r1(b, c, d, a, (i * 16) + 15, 19, x)

            # второй раунд
            a = r2(a, b, c, d, (i * 16) + 0, 3, x)
            d = r2(d, a, b, c, (i * 16) + 4, 5, x)
            c = r2(c, d, a, b, (i * 16) + 8, 9, x)
            b = r2(b, c, d, a, (i * 16) + 12, 13, x)
            a = r2(a, b, c, d, (i * 16) + 1, 3, x)
            d = r2(d, a, b, c, (i * 16) + 5, 5, x)
            c = r2(c, d, a, b, (i * 16) + 9, 9, x)
            b = r2(b, c, d, a, (i * 16) + 13, 13, x)
            a = r2(a, b, c, d, (i * 16) + 2, 3, x)
            d = r2(d, a, b, c, (i * 16) + 6, 5, x)
            c = r2(c, d, a, b, (i * 16) + 10, 9, x)
            b = r2(b, c, d, a, (i * 16) + 14, 13, x)
            a = r2(a, b, c, d, (i * 16) + 3, 3, x)
            d = r2(d, a, b, c, (i * 16) + 7, 5, x)
            c = r2(c, d, a, b, (i * 16) + 11, 9, x)
            b = r2(b, c, d, a, (i * 16) + 15, 13, x)

            # третий раунд
            a = r3(a, b, c, d, (i * 16) + 0, 3, x)
            d = r3(d, a, b, c, (i * 16) + 8, 9, x)
            c = r3(c, d, a, b, (i * 16) + 4, 11, x)
            b = r3(b, c, d, a, (i * 16) + 12, 15, x)
            a = r3(a, b, c, d, (i * 16) + 2, 3, x)
            d = r3(d, a, b, c, (i * 16) + 10, 9, x)
            c = r3(c, d, a, b, (i * 16) + 6, 11, x)
            b = r3(b, c, d, a, (i * 16) + 14, 15, x)
            a = r3(a, b, c, d, (i * 16) + 1, 3, x)
            d = r3(d, a, b, c, (i * 16) + 9, 9, x)
            c = r3(c, d, a, b, (i * 16) + 5, 11, x)
            b = r3(b, c, d, a, (i * 16) + 13, 15, x)
            a = r3(a, b, c, d, (i * 16) + 3, 3, x)
            d = r3(d, a, b, c, (i * 16) + 11, 9, x)
            c = r3(c, d, a, b, (i * 16) + 7, 11, x)
            b = r3(b, c, d, a, (i * 16) + 15, 15, x)

            self.A = self.A + a & 0xffffffff
            self.B = self.B + b & 0xffffffff
            self.C = self.C + c & 0xffffffff
            self.D = self.D + d & 0xffffffff

        result = list(pack('<I', self.A)) + list(pack('<I', self.B)) + list(pack('<I', self.C)) + list(pack('<I', self.D))
        return ''.join([str("0x%02x" % x)[2:] for x in result])

    def avalanche_effect(self, msg):
        self.expand_message(msg)
        res_hash = self.rounds_f()
        hash_to_bit = int_to_bin(self.A, self.B, self.C, self.D)

        return res_hash, msg, hash_to_bit


def check1(msg, right):
    A = md4()
    A.expand_message(msg)
    my_result = A.rounds_f()

    print('мой:', my_result, '|правильный', right)


def check2(msg):
    A = md4()
    B = md4()
    word = msg
    mod_word = change_random_bit(word)

    word = A.avalanche_effect(word)
    mod_word = B.avalanche_effect(mod_word)

    dif_bits = 0
    for i in range(0, len(word[2])):
        if word[2][i] ^ mod_word[2][i]:
            dif_bits += 1
    print((word[0], word[1]))
    print((mod_word[0], mod_word[1]))

    print(dif_bits)


def check3(k, l):
    word_list = []
    hash_list = []
    flag = True
    index = 0

    while flag:
        msg = ''
        for i in range(0, l):
            msg += chr(randint(32, 126))

        A = md4()
        A.expand_message(msg)
        A.rounds_f()

        temp = bin(A.A)[2:]
        while len(temp) % k != 0:
            temp = '0' + temp

        h = temp[len(temp) - k:]

        if h not in hash_list:
            word_list.append(msg)
            hash_list.append(h)
        elif h in hash_list:
            flag = False
            word_list.append(msg)
            hash_list.append(h)
            print(h)
            for i in range(0,len(hash_list)):
                if hash_list[i] == h:
                    index = i
                    break

            # первое слово
            word_A = word_list[index]
            print(hash_list[index])
            A = md4()
            A.expand_message(word_A)
            hash_A = A.rounds_f()

            # второе слово
            word_B = msg
            B = md4()
            B.expand_message(word_B)
            hash_B = B.rounds_f()


    print(word_A, hash_A)
    print(word_B, hash_B)
    print(len(word_list))


def check3_paint(k, l):
    word_list = []
    hash_list = []
    flag = True
    index = 0

    while flag:
        msg = ''
        for i in range(0, l):
            msg += chr(randint(32, 126))

        A = md4()
        A.expand_message(msg)
        A.rounds_f()

        temp = bin(A.A)[2:]
        while len(temp) % k != 0:
            temp = '0' + temp

        h = temp[len(temp) - k:]

        if h not in hash_list:
            word_list.append(msg)
            hash_list.append(h)
        elif h in hash_list:
            flag = False
            word_list.append(msg)
            hash_list.append(h)

            for i in range(0,len(hash_list)):
                if hash_list[i] == h:
                    index = i
                    break

            # первое слово
            word_A = word_list[index]

            A = md4()
            A.expand_message(word_A)
            hash_A = A.rounds_f()

            # второе слово
            word_B = msg
            B = md4()
            B.expand_message(word_B)
            hash_B = B.rounds_f()

    return len(word_list)


def check4(k, text):
    A = md4()
    A.expand_message(text)
    h_A = A.rounds_f()

    temp = bin(A.A)[2:]
    while len(temp) % k != 0:
        temp = '0' + temp

    k_A = temp[len(temp) - k:]

    flag = True
    count = 0
    while flag:
        msg = ''
        for i in range(0, len(text)):
            msg += chr(randint(32, 126))

        count += 1

        B = md4()
        B.expand_message(msg)
        h_B = B.rounds_f()

        temp = bin(B.A)[2:]
        while len(temp) % k != 0:
            temp = '0' + temp

        k_B = temp[len(temp) - k:]

        if k_B == k_A:
            flag = False
            print('Исходная строка и ее Хэш:', text, h_A)
            print('Прообраз исходной строки:', msg, h_B)
            print('Количество операций:', count)


def check4_paint(k, text):
    A = md4()
    A.expand_message(text)
    h_A = A.rounds_f()

    temp = bin(A.A)[2:]
    while len(temp) % k != 0:
        temp = '0' + temp

    k_A = temp[len(temp) - k:]

    flag = True
    count = 0
    while flag:
        msg = ''
        for i in range(0, len(text)):
            msg += chr(randint(32, 126))

        count += 1

        B = md4()
        B.expand_message(msg)
        h_B = B.rounds_f()

        temp = bin(B.A)[2:]
        while len(temp) % k != 0:
            temp = '0' + temp

        k_B = temp[len(temp) - k:]

        if k_B == k_A:
            flag = False

    return count


print('Первое задание'.center(50))
check1('', '')
check1("", '31d6cfe0d16ae931b73c59d7e0c089c0')
check1("abc", 'a448017aaf21d8525fc10ae87aa6729d')
check1("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", '043f8582f241db351ce627e153e7f0e4')
print('-' * 82)


print('Второе задание'.center(50))
check2("abc")
check2("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
print('-' * 82)

print('Третье задание'.center(50))
check3(16, 5)
print('-' * 82)

'''Третье задание. График'''
y = []
x = [k for k in range(1, 33)]

for k in x:
    y.append(check3_paint(k, 5))
paint(x, y, 'N', 'K')
'''end 3'''


print('Четвертое задание'.center(50))
# check4(16,'123456')
print('-' * 82)

'''Четвертое задание. График'''
# y = []
# x = [k for k in range(1, 21)]
#
# for k in x:
#     print(k)
#     y.append(check4_paint(k, 'abcde'))
# paint(x, y, 'N', 'K')
'''end 4'''
