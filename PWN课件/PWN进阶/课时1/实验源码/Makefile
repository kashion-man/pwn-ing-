all: house_of_orange_challenge

house_of_orange_challenge: house_of_orange_challenge.c
	gcc -fPIC -pie -z relro -z now house_of_orange_challenge.c -o house_of_orange_challenge

clean:
	rm -f house_of_orange_challenge
	