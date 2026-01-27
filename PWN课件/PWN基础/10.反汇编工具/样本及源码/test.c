#include<stdio.h>
int func(int a,int b){
    int rel;
    rel = a + b;
    return rel;
}


int main(){
    int sum,a,b;
    char buf[] = "Welcome to IDA!\n";
    printf("%s",buf);
    puts("Input a and b");
    scanf("%d %d",&a,&b);
    sum = func(a,b);
    if(sum > 100){
        sum = sum - 100;
        printf("The new sum: %d\n",sum);
    }
    else if(sum < 10){
        sum = sum + 100;
        printf("The new sum: %d\n",sum);
    }
    else{
        printf("The sum: %d\n",sum);
    }
    return 0;
}