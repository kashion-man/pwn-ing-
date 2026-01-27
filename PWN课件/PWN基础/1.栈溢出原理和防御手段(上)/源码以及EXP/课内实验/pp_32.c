#include<stdio.h>
int add(int a,int b){
    return a+b;
}

int main(){
    int a = 4;
    int b = 5;
    int sum ;
    sum = add(a,b);
    printf("sum: %d\n",sum);
    return 0;
}
