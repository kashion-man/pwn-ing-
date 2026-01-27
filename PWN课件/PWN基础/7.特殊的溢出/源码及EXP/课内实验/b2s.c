#include<stdio.h>
void back(int i){
    if(i == 0){
        printf("Yes!\n");    
    }
    else{
        printf("NO!\n");
    }
}

int main(){
    long int a;
    scanf("%ld",&a);
    if(a == 0){
        printf("Error!\n");
    }
    else{
        back(a);
    }
    return 0;
}
