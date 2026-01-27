#include<stdio.h>



char mychar[]={"abcdefghijkl"};

int main(int argc, char *argv[])
{
    int a = 0x11223344;
    int b = 0x55667788;
    char c[]= "abcde";
    char temps[256]={0};
    printf("please input your str:");
    scanf("%s", temps);
    if(strcmp(temps,c) == 0)
    {
        printf("1");
    }else{
        printf("2");
    }
    return 0;
}