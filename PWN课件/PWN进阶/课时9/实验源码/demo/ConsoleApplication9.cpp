#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <Windows.h>

void backdoor() {
	system("cmd.exe");
}

int main() {
	setbuf(stdout, 0);
	setbuf(stderr, 0);
	setbuf(stdin, 0);
	char buf[0x20];
	printf("gift=0x%lx\n", backdoor);
	__try {
		printf("input a:");
		scanf("%s", buf);
		int a = atoi(buf);
		printf("input b:");
		scanf("%s", buf);
		int b = atoi(buf);
		printf("ans=%d\n",a / b);

	}
	__except (GetExceptionCode() == EXCEPTION_INT_DIVIDE_BY_ZERO ? EXCEPTION_EXECUTE_HANDLER : EXCEPTION_CONTINUE_SEARCH) {
		puts("try to solve");
	}
	exit(0);
} 