#include <stdio.h>
void getshell(void) {
    system("/bin/sh");
}
void init() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int main(void) {
    init();
    puts("Tell me your name:");
    char name[16];
    char buf[40];
    read(0,name,25);
    puts("Nice to see you:");
    printf(name);
    puts("What do you want to tell me:");
    read(0,buf,0x50);
    printf("OK! I already know!");
    return 0;
}
