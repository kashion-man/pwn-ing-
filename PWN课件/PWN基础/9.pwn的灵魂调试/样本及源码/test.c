#include<stdio.h>
int checkpw(char *str){
    if(strcmp(str,"easy_test\n") == 0){
        printf("You are right!\n");
    }
    else{
        printf("NO!\n");
    }
    return 0;
}

int main(){
    char str[100];
    memset(str,'0',100);
    read(0,str,99);
    printf("%s\n",str);
    checkpw(&str);
    return 0;
}
