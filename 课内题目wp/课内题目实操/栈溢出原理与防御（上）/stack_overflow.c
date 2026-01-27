#include<stdio.h>
void pwnme(){
    system("/bin/sh");
}


int main(){
    char buf[10];
    gets(buf);
    printf("%s\n",&buf);
    return 0;
}
