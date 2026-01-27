#include<stdio.h>
int main(){
    short int a = 0x7fff;
    printf("a: %x, a: %d\n",a,a);
    a = a + 1;
    printf("a: %x, a: %d\n",a,a);
    return 0;
}
