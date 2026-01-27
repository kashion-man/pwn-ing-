#include<stdio.h>
int main(){
    char str[100];
    while(1){
        memset(&str,0,0x64);
        read(0,&str,0x63);
        printf(str);
    }
    return 0;
}
