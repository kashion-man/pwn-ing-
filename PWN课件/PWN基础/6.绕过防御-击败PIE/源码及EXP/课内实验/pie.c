#include<stdio.h>
void fun(){
    printf("Hello World\n");
}

int main(){
    printf("add_addr: %p\n",(void *)*fun);
    return 0;
}
