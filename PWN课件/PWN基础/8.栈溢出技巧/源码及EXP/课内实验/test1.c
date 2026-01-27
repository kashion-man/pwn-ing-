#include<stdio.h>
char all[100];

void back(){
    printf("/bin/sh");
    system("exit");
}

int main(){
    char buf[10];
    printf("Hello,tell me your story:\n");
    read(0,&all,0x63);
    printf("By the way, what's your name:\n");
    read(0,&buf,0x10);
    return 0;
}
