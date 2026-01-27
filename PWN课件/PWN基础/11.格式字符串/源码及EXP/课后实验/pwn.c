#include<stdio.h>
void shell(){
    system("echo sir");
}

int main(){
    char format[80];
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    puts("Hello sir! What's your name?");
    read(0,format,80);
    printf(format);
    puts("Ok! What do you want to tell me?");
    scanf("%70s", &format);
    printf("%s\n",&format);
    return 0;
}