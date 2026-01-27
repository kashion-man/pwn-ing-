#include<stdio.h>
#include<stdlib.h>
int main(){
    char *str1 = malloc(100);
    read(0,str1,80);
    printf("%s",str1);
    char *str2 = malloc(100);
    char *str3 = malloc(100);
    free(str1);
    free(str2);
    return 0;
}