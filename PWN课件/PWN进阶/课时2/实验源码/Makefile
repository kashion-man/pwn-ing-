all: tcache_corruption_challenge

tcache_corruption_challenge: tcache_corruption_challenge.c task.c task.h
	gcc -fPIC -pie -z relro -z now tcache_corruption_challenge.c task.c -o tcache_corruption_challenge -pthread

clean:
	rm -f tcache_corruption_challenge
	