#include<stdio.h>
int main()
{
        int a = 0,b = 0,c = 0;
        printf("ABC%nEFG%n\n",&a,&b);
        printf("%123c%n\n",'a',&c);
        printf("a=%d b=%d c=%d\n",a,b,c);
        return 0;
}