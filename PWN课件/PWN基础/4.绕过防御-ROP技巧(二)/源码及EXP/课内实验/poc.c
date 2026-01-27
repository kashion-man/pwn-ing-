#include<stdio.h>
#include<unistd.h>;

void init() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    alarm(100);
}

void vuln(){
    char buf[40];
    read(0,buf,0x100);
}

int main(){
    init();
    vuln();
    return 0;
}