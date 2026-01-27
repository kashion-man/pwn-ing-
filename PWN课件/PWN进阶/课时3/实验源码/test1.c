#include <stdio.h>
#include <stdlib.h>

char buf[0x100];
int main() {
   char *p1 = malloc(0x400 - 0x10);
   char *gap = malloc(0x10); //gap
   char *p2 = malloc(0x410 - 0x10);
   gap = malloc(0x10);
   char *p3 = malloc(0x420 - 0x10);
   gap = malloc(0x10);
   free(p1);
   free(p2);
   free(p3);
   malloc(0x500);
   read(0,buf,0x100);
}
