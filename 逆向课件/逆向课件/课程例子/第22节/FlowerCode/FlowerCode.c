#include<stdio.h>
#include<string.h>
int main() {
	puts("Looks like trouble,do you know junkcode?");
	//1. jz/jnz跳转
	__asm {
		jz label0
		jnz label0
		__emit 0xe8
		label0:
	}
	puts("Plz input your flag:");
	unsigned char key[9] = "JunkCode";
	unsigned char input[29] = { 0 };
	//2. 永真永假条件跳转
	__asm {
		push ebx
		xor ebx, ebx
		test ebx, ebx
		jnz label1
		jz label2
	label1 :
		_emit 0xc2
	label2 :
		pop ebx//需要恢复ebx寄存器    
	}
	//flag{S0-be@ut1fUl-f10weRs}
	unsigned char data[28] = { 0x2c,0x19,0xf,0xc,0x38,0x3c,0x54,0x48,0x28,0x10,0x2e,0x1e,0x37,0x5e,0x2,0x30,0x26,0x58,0x8,0x5a,0x73,0x18,0x1,0x37,0x39,0x8,0x6e };

	scanf("%s", input);
	//3. call&ret
	__asm {
		call label3
		_emit 0xe8
	label3:
		add dword ptr ss : [esp] , 8;//变长指令
		ret
		_emit 0xe8
	}

	for (int i = 0; i < 27; i++)
	{
		input[i] ^= key[i % 8];
	}
	if (memcmp(input, data, 28) == 0) {
		printf("Good!\n");
	}
	else
		printf("TryAgain!\n");
	return 0;
}