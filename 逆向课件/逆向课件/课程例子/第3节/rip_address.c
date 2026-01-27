#include <stdint.h>



int64_t x2 = 0xbb;
int64_t add(int64_t a, int64_t b)
{
    x2 = 0xcc;
    return a + b;
}