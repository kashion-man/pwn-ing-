#include<stdio.h>
void shell_pwn(){
    system("/bin/sh");
}

int main(){
    char buf[120];
    gets(buf);
    printf("buf: %s\n",buf);
    return 0;
}
