#include <stdio.h>
#include <unistd.h>

int main(){
    char buffer[0x10] = {0};
    setvbuf(stdout, NULL, _IOLBF, 0);
    printf("This is your gift : [%p]\n", buffer);
    read(0, buffer, 0x40);
    return 0;
}