#include<stddef.h>
int main(void)
{
    int len;
    int data_len;
    int buf_len;
    char *buf;

    buf_len = 0x10;
    scanf("%uld", &data_len);

    len = data_len + buf_len;
    buf = malloc(len);
    read(0, buf, data_len);
    return 0;
}