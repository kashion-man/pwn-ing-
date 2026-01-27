#include <stdio.h>



int main(int argc, char *argv[])
{
    printf("hello, I am here!\n");
    printf("I will stop until your inputs\n");
    char input[1024]={0};
    read(0, input, 500);
    printf("%s\n", input);
    return 0;
}