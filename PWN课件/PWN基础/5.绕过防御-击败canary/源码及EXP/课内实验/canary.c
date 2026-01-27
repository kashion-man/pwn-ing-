#include<stdio.h>
int main(){
    char buf[8];
    read(0,&buf,0x20);
    printf("%s\n",buf);
    return 0;
}
