#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
void getshell() {
    system("/bin/sh");
}
void init() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}
void fun() {
    char buf[32];
    for(int i=0;i<2;i++){
        read(0, buf, 100);
        printf(buf);
    }
}
int main() {
    init();
    puts("Welcome!");
    fun();
    return 0;
}