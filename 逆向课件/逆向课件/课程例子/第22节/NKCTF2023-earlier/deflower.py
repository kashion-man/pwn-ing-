import idc
import idautils
import ida_bytes
pattern = "33 C0 85 C0 74 03 75 00 E8" 	# 匹配花指令字节码
cur_addr = 0x401000						# 程序起始地址
while cur_addr != idc.BADADDR:			# 遍历程序可访问地址
    cur_addr = idc.find_binary(cur_addr,SEARCH_DOWN,pattern) 
    # 匹配花指令所在地址,第一个参数是起始地址,第二个参数是搜索方式,这里是向下(低地址向高地址搜索),第三个是格式字符串
    if cur_addr == idc.BADADDR:								 # 如果未匹配到
        break;
    else:
        print("patch address: ",hex(cur_addr)) 				 # 打印起始地址
        for i in range(9):									 # 开始patch
            ida_bytes.patch_byte(cur_addr,0x90)
            cur_addr += 1
