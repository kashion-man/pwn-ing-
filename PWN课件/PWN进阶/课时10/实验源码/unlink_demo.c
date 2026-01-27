#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define MAX_COUNT 0x10

int menu() {
	puts("1.add");
	puts("2.delete");
	puts("3.show");
	puts("4.edit");
	puts("5.exit");
	printf(">>");
	int choice;
	scanf("%d",&choice);
	return choice;
}
char *heaps[MAX_COUNT] = {0};
int heap_size[MAX_COUNT] = {0};

int getIndex() {
	int i;
	for (i=0; i<MAX_COUNT; i++) {
		if (!heaps[i]) {
			return i;
		}
	}
	if (i == MAX_COUNT) {
		puts("no space!");
		exit(-1);
	}
}

void add() {
	int i = getIndex();
	printf("size:");
	unsigned int size;
	scanf("%d",&size);
	if (size > 0x100) {
		puts("too large");
		return;
	}
	heaps[i] = (char *)malloc(size);
	if (!heaps[i]) {
		puts("malloc error!");
		exit(-1);
	}
	heap_size[i] = size;
	printf("content:");
	read(0,heaps[i],size);
	puts("done");
}

void backdoor() {
	system("cmd.exe");
}
void del() {
	printf("index:");
	unsigned int index;
	scanf("%d",&index);
	if (index > MAX_COUNT || !heaps[index]) {
		puts("invalid index");
		return;
	}
	free(heaps[index]);
	heaps[index] = 0; 
}

void show() {
	printf("index:");
	unsigned int index;
	scanf("%d",&index);
	if (index > MAX_COUNT || !heaps[index]) {
		puts("invalid index");
		return;
	}
	puts(heaps[index]);
}

void edit() {
	printf("index:");
	unsigned int index;
	scanf("%d",&index);
	if (index > MAX_COUNT || !heaps[index]) {
		puts("invalid index");
		return;
	}
	printf("content:");
	read(0,heaps[index],heap_size[index]+0x8);
	puts("done");
}
int main() {
	setbuf(stdout,0);
	setbuf(stdin,0);
	setbuf(stderr,0); 
	char buf[0x20];
	printf("what is your name:");
	read(0,buf,0x20);
	printf("gift:0x%p\n",backdoor); 

	while (1) {
		switch(menu()) {
			case 1:
				add();
				break;
			case 2:
				del();
				break;
			case 3:
				show();
				break;
			case 4:
				edit();
				break;
			case 5:
				return 0;

		}
	}
}
