#include <stdio.h>
#include <stdlib.h>

char name[0x60];

void fun() {
        puts("what do you want to say:");
	char buf[0x20];
	read(0,buf,0x100);
}

int main() {
	puts("welcome to haivk's class");
	puts("what is your name:");
	read(0,name,0x60);
	fun();
}
