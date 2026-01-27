#include <stdio.h>
#include <stdlib.h>

int fun(int a,int b,int c,int d,int e,int f,int g,int h,int i,int j,int k,int l) {
	printf("%d %d %d %d\n",a,b,c,d);
	return 1;
}

int main() {
        fun(1,2,3,4,5,6,7,8,9,10,11,12);
	return 0;
}
