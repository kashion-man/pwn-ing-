#include<stdio.h>
void init(){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int main(){
    char name[56];
    char buf[112];
    init();
    puts("Welcome to Pie!");
    puts("Tell me your name:");
    read(0,name,49);
    printf("Your name is %s\n",name);
    puts("What do you want to say?");
    read(0,buf,0x100);
    puts("Bye!");  
    return 0;
}
