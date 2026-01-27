#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char buf[0x100] = {0};
int main() {
   char *p1 = malloc(0x10);
   char *top_chunk_addr = p1 + 0x10;
   *(size_t *)(top_chunk_addr + 0x8) = -1; //修改top chunk的size
   size_t offset = buf - p1 - 0x30;
   malloc(offset);
   char *p2 = malloc(0x50);
   strcpy(p2,"hello,welcome to haivk's class\n");
   write(1,buf,strlen(buf));
   return 0;
}
