#include<stdio.h>
#include<Windows.h>
#include<string.h>

//flag{Y0u-@re-v3ry-kNow-smc-ahd-x0r}
unsigned char data[40] = { 0x00,0x0a,0x07,0x01,0x1d,0x3f,0x56,0x13,0x4b,0x26,0x14,0x03,0x4b,0x10,0x55,0x14,0x1f,0x4b,0x0d,0x28,0x09,0x11,0x4b,0x15,0x0b,0x05,0x4b,0x07,0x0e,0x02,0x4b,0x1e,0x56,0x14,0x1b,0 };
void func(unsigned char* input,int len ) {
	for (int i = 0; i < 35; i++) { 
		input[i] ^= 0x66; 
	}
}
int main() {
	static DWORD oldProtect = 0;	
	static SIZE_T codeLen = 0;		//定义为静态变量防止被优化
	byte* funcAddr = (byte*)func;	//取函数首地址用于SMC解密
	unsigned char input[40] = { 0 };
	int flagLen = 39;
	printf("Plz input your flag:");
	scanf("%39s", input);
	//SMC解密func函数
	VirtualProtect(func, codeLen, PAGE_EXECUTE_READWRITE, &oldProtect);//CodeLen可以编译后通过ida查看得到,手动patch即可
	for (int i = 0; i < codeLen; i++)//解密操作,但编译期间并未加密,需要手动加密
		funcAddr[i] ^= 0x66;
	VirtualProtect(func, codeLen, oldProtect, &oldProtect);
	func(input,flagLen);
	if (memcmp(data, input, flagLen) == 0)
		printf("Good!");
	else
		printf("Try again!");
	return 0;
}