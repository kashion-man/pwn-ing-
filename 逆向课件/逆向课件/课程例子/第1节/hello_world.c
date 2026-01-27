#include <stdio.h>
#include <stdint.h>

char temps[]={"abcdefghijkl"};
int32_t a = 0xaabbccdd;

int main()
{
    int x=0;
    int y = 10;
    printf("hello_world!\n");
    printf("%s", temps);
    printf("%d", a);
    signed int x1=100;
    signed int x2=30;
    signed int result;

    result = x1 + x2;
    result = x1 - x2;
    result = x1 * x2;
    result = x1 / x2;
    result = x1 % x2;
    result = x1 << 10;
    result = x1 >> 10;
    // unsigned int

    unsigned int y1 = 200;
    unsigned int y2 = 40;
    unsigned int result2;

    result2 = y1 + y2;
    result2 = y1 - y2;
    result2 = y1 * y2;
    result2 = y1 / y2;
    result2 = y1 % y2;
    result2 = y1 << 10;
    result2 = y1 >> 10;

    return 0;
}