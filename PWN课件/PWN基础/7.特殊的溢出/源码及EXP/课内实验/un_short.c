#include<stdio.h>
int main(){
    unsigned short int b = 0xffff;
    printf("b: %d, b: %x\n",b,b);
    b = b + 1;
    printf("b: %d, b: %x\n",b,b);
    return 0;
}
