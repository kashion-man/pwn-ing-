#include<stdio.h>
char name[16] = {0};
void hi(){
    system("whoami");
}
int main(){
    char buf[80];
    read(0,name,10);
    printf("Hello sir: %s",&name);
    read(0,buf,0x100);
    printf("May be you can try again!\n");
    return 0;
}