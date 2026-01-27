#include<stdio.h>
#include <stdlib.h>
void init() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int first()
{
  int v1,v2;
  char num_x[40],num_y[40];
  memset(&num_x, 0, 0x10);
  puts("x: ");
  read(0, &num_x, 0x10);
  puts("y: ");
  read(0, &num_y, 0x10);
  if(strchr(&num_x, '-') || strchr(&num_y, '-')){
      return 0;
  }
  v1 = atoi(&num_x);
  v2 = atoi(&num_y);
  if ( v1 > 359 || v2 > 359 || v1 - v2 != 520 ){
      return 0;
  }
  puts("first function success!");
  return 1;
}

int second(){
  int v1 = 0;
  int v2 = 0;
  puts("Please input x and y:");
  scanf("%d %d", &v1, &v2);
  if(v1 > 1 && v2 > 520 && v1 * v2 == 520){
        puts("second function success!");
        return 1;
  }
  return 0;
}

int main(){
    init();
    if(first() && second()){
        system("/bin/sh");
    }
    return 0;
}