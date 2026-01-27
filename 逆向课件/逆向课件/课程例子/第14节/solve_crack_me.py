#!/usr/bin/env python3


def encrypt(key, seed, string):
    rst = []
    for v in string:
        rst.append((ord(v) + seed ^ ord(key[seed])) % 255)
        seed = (seed + 1) % len(key)
    return rst

print("Welcome python crackme")
flag = input('Enter the Flag: ')
KEY1 = 'Maybe you are good at decryptint Byte Code, have a try!'
KEY2 = [75, 11, 7, 26, 164, 31, 1, 16, 160, 10, 23, 236, 20, 88, 30, 1, 92, 247]
en_out = encrypt(KEY1, 5, flag)
if KEY2 == en_out:
    print('You Win')
else:
    print('Try Again !')
