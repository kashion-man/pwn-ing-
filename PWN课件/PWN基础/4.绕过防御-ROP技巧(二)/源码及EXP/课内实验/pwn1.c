#include <unistd.h>
#include <stdio.h>
#include <string.h>

void fun()
{
        char buf[100];
        setbuf(stdin, buf);
        read(0, buf, 256);
}

int main()
{
        char buf[100] = "Nice to meet you~!\n";
        setbuf(stdout, buf);
        write(1, buf, strlen(buf));
        fun();
        return 0;
                        
}
