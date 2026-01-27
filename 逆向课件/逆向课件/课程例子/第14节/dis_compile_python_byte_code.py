#!/usr/bin/env python3
import dis

def secret(a, b, c, d):
    print(a + b)
    print(a - b)
    print(a * d)
    print(a / b)
    print(a % c)
    print(a + b - c * d)
    ccc = len([a, b, c, d])
    return



print(dis.dis(secret))