#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char buf[0x100] = {0};
int main() {
   char *p1 = malloc(0x10);
   char *top_chunk_addr = p1 + 0x10;
   *(size_t *)(top_chunk_addr + 0x8) = 0xFE1; //修改top chunk的size，注意页对齐
   malloc(0x1000);
   read(0,buf,0x100);
   return 0;
}
